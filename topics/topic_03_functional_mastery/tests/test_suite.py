"""Tests for Topic 03: Functional Mastery."""
from __future__ import annotations
import unittest
from pathlib import Path
from topics.topic_03_functional_mastery.concepts.closures import make_event_counter, make_severity_tracker, make_source_filter
from topics.topic_03_functional_mastery.concepts.decorators import annotate_stage, require_event_fields
from topics.topic_03_functional_mastery.concepts.higher_order import filter_events as ho_filter_events, map_events, reduce_counts
from topics.topic_03_functional_mastery.concepts.lambda_predicates import filter_events, has_tag, severity_at_least
from topics.topic_03_functional_mastery.concepts.partial_application import add_constant_field, make_region_enricher, prefix_message
from topics.topic_03_functional_mastery.concepts.pure_composition import add_tag, cap_severity, compose as pure_compose, normalize_message, pipe as pure_pipe
from topics.topic_03_functional_mastery.dsa.closure_counters import make_counter, make_key_counter, make_rate_limiter
from topics.topic_03_functional_mastery.dsa.decorator_validators import validate_event_fields, validate_severity_range, validated_transform
from topics.topic_03_functional_mastery.dsa.pipeline import Pipeline, compose, pipe
from topics.topic_03_functional_mastery.dsa.predicate_filters import all_of, any_of, filter_records, not_, partition_records
from topics.topic_03_functional_mastery.errors.callable_contracts import apply_transform, ensure_callable
from topics.topic_03_functional_mastery.errors.decorator_metadata import callable_name, safe_trace, unsafe_trace
from topics.topic_03_functional_mastery.errors.functional_defensive_patterns import FunctionalPipelineError, safe_pipe
from topics.topic_03_functional_mastery.errors.lambda_readability import is_overly_complex_lambda, named_severity_and_tag, readability_advice
from topics.topic_03_functional_mastery.errors.late_binding_closures import build_bad_tag_checkers, build_tag_checkers, build_tag_checkers_factory
from topics.topic_03_functional_mastery.solutions.advanced_solution import run_functional_ingestion
from topics.topic_03_functional_mastery.solutions.entry_solution import build_entry_pipeline
from topics.topic_03_functional_mastery.solutions.mid_solution import critical_alerts, enrich_valid_event

def event(event_id='evt-1', source='sensor.edge-7', severity=3, message=' HOT  DISK ', tags=None, metadata=None):
    return {'event_id': event_id, 'source': source, 'severity': severity, 'message': message, 'tags': ['edge'] if tags is None else tags, 'metadata': {'region': 'eu-west'} if metadata is None else metadata}

class ConceptHelperTests(unittest.TestCase):
    def test_closures_decorators_predicates_higher_order_partial_and_pure_helpers(self):
        counter = make_event_counter(); self.assertEqual([counter(event()), counter(event())], [1, 2]); self.assertTrue(make_source_filter('sensor.edge-7')(event()))
        tracker = make_severity_tracker(); self.assertEqual(tracker(event(severity=4)), {4: 1}); snapshot = tracker(event(severity=4)); snapshot[4] = 99; self.assertEqual(tracker(event(severity=1)), {4: 2, 1: 1})
        @require_event_fields(('event_id', 'message'))
        @annotate_stage('checked')
        def clean(record):
            """Preserved doc."""
            return {**record, 'message': record['message'].strip()}
        self.assertEqual(clean(event())['stages'], ('checked',)); self.assertEqual(clean.__name__, 'clean')
        with self.assertRaises(KeyError): clean({'event_id': 'missing'})
        records = [event('evt-1', severity=2), event('evt-2', severity=5, tags=['edge', 'security']), event('evt-3', source='api', severity=4)]
        self.assertEqual([r['event_id'] for r in filter_events(records, severity_at_least(4))], ['evt-2', 'evt-3']); self.assertEqual([r['event_id'] for r in filter_events(records, has_tag('security'))], ['evt-2'])
        self.assertEqual(len(ho_filter_events(records, lambda r: r['source'] == 'sensor.edge-7')), 2); self.assertTrue(all(r['mapped'] for r in map_events(records, lambda r: {**r, 'mapped': True}))); self.assertEqual(reduce_counts(records, lambda r: r['source']), {'sensor.edge-7': 2, 'api': 1})
        self.assertEqual(add_constant_field(records[0], 'region', 'us')['region'], 'us'); self.assertEqual(prefix_message('ALERT: ', records[0])['message'], 'ALERT:  HOT  DISK '); self.assertEqual(make_region_enricher('ap')(records[0])['region'], 'ap')
        original = event(severity=9, tags=['edge'], metadata={'region': 'eu'}); result = pure_pipe(original, normalize_message, cap_severity, lambda r: add_tag(r, 'processed'))
        self.assertEqual((result['message'], result['severity'], result['tags']), ('hot disk', 5, ('edge', 'processed'))); original['metadata']['region'] = 'changed'; self.assertEqual(result['metadata'], {'region': 'eu'}); self.assertEqual(original['tags'], ['edge']); self.assertEqual(pure_compose(lambda x: x + 1, lambda x: x * 2)(3), 7)

class DsaHelperTests(unittest.TestCase):
    def test_pipeline_predicates_validators_and_counters(self):
        self.assertEqual(compose(lambda x: x + 1, lambda x: x * 2)(3), 7); self.assertEqual(pipe(3, lambda x: x + 1, lambda x: x * 2), 8); self.assertEqual(Pipeline([lambda x: x + 2]).then(lambda x: x * 3)(4), 18)
        with self.assertRaises(TypeError): Pipeline([lambda x: x, 3])
        records = [event('evt-1', severity=2), event('evt-2', severity=5, tags=['security'])]; pred = all_of(lambda r: r['severity'] >= 4, lambda r: 'security' in r['tags'])
        self.assertEqual(filter_records(records, pred), [records[1]]); self.assertTrue(any_of(lambda r: r['severity'] == 2, lambda r: False)(records[0])); self.assertFalse(not_(lambda r: r['severity'] == 2)(records[0])); self.assertEqual(partition_records(records, pred), ([records[1]], [records[0]]))
        @validated_transform(validate_event_fields(('event_id', 'severity')), validate_severity_range())
        def mark(record): return {**record, 'marked': True}
        self.assertTrue(mark(event())['marked']); self.assertEqual(mark.__name__, 'mark')
        with self.assertRaises(ValueError): mark(event(severity=6))
        c = make_counter(10); self.assertEqual([c(), c()], [11, 12]); kc = make_key_counter(lambda r: r['source']); self.assertEqual(kc(event(source='a')), {'a': 1}); self.assertEqual(kc(event(source='a')), {'a': 2}); limiter = make_rate_limiter(1); self.assertEqual([limiter('a'), limiter('b')], [True, False])

class ErrorBehaviorTests(unittest.TestCase):
    def test_error_modules_demonstrate_failures_and_defenses(self):
        record = event(tags=['edge']); self.assertEqual([fn(record) for fn in build_bad_tag_checkers(['edge', 'security'])], [False, False]); self.assertEqual([fn(record) for fn in build_tag_checkers(['edge', 'security'])], [True, False]); self.assertEqual([fn(record) for fn in build_tag_checkers_factory(['edge', 'security'])], [True, False])
        def stage(record): return record
        self.assertEqual(callable_name(unsafe_trace(stage)), 'wrapper'); self.assertEqual(callable_name(safe_trace(stage)), 'stage')
        dense = "lambda record: record.get('severity', 0) >= 4 and 'edge' in record.get('tags', ()) or record.get('source') == 'backup'"; self.assertTrue(is_overly_complex_lambda(dense)); self.assertEqual(readability_advice(dense), 'replace with a named predicate helper'); self.assertTrue(named_severity_and_tag(4, 'edge')(event(severity=4)))
        with self.assertRaisesRegex(TypeError, 'callback must be callable'): ensure_callable(12)
        with self.assertRaisesRegex(TypeError, 'mapping-like'): apply_transform(event(), lambda r: 3)
        def boom(value): raise ValueError('boom')
        with self.assertRaises(FunctionalPipelineError) as ctx: safe_pipe(1, boom)
        self.assertIsInstance(ctx.exception.__cause__, ValueError)

class SolutionAndLabTests(unittest.TestCase):
    def test_solutions_and_full_advanced_smoke_test(self):
        source = event(severity=8, message=' MIXED  CASE ', tags=['edge']); self.assertEqual(build_entry_pipeline([source])[0]['tags'], ('edge', 'processed')); self.assertEqual(source['tags'], ['edge'])
        self.assertIn('validated', enrich_valid_event(event())['tags']); self.assertEqual([r['event_id'] for r in critical_alerts([event('lo', severity=2), event('hi', severity=5)], 4)], ['hi'])
        batch = [event('evt-1', source='sensor.edge-7', severity=5, message=' CPU  HOT ', tags=['edge']), event('evt-2', source='api.gateway', severity=4, message=' AUTH  FAIL ', tags=['security'], metadata={'region': 'us-east'}), event('evt-3', source='sensor.edge-7', severity=2, message=' ok ', tags=['edge']), event('bad', source='sensor.bad', severity=9, tags=['bad'])]
        original_tags = [list(r['tags']) for r in batch]; original_messages = [r['message'] for r in batch]; result = run_functional_ingestion(batch)
        self.assertEqual(result['accepted_count'], 3); self.assertEqual(len(result['rejected']), 1); self.assertEqual(result['counts_by_source'], {'sensor.edge-7': 2, 'api.gateway': 1}); self.assertEqual([e['message'] for e in result['events']], ['cpu hot', 'auth fail', 'ok']); self.assertTrue(all('ingested' in e['tags'] for e in result['events'])); self.assertEqual([r['tags'] for r in batch], original_tags); self.assertEqual([r['message'] for r in batch], original_messages)
    def test_lab_files_are_prompt_only(self):
        lab_dir = Path('topics/topic_03_functional_mastery/lab'); self.assertEqual({p.name for p in lab_dir.glob('*.md')}, {'entry_challenge.md', 'mid_challenge.md', 'advanced_challenge.md'})
        for path in lab_dir.glob('*.md'):
            text = path.read_text(encoding='utf-8')
            for marker in ('def ', 'class ', 'return '): self.assertNotIn(marker, text)

if __name__ == '__main__': unittest.main()
