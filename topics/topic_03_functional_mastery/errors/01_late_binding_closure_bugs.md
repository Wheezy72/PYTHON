# Late-Binding Closure Bugs

Failure mode: closures capture variables by reference, not by value. If SentinelFlow builds route predicates or transformers inside a loop, every generated function may observe the loop variable's final value.

SentinelFlow example: creating one transformer per route in a loop can accidentally make every transformer add the last route, sending all events to the wrong audit destination.

Defensive pattern: use a stage factory such as `add_route(route)` so each call captures one route, or bind the current value as a default argument in very small lambdas. Test every generated function, not just the last one.

Complexity impact: factory creation is O(1) per generated stage. Storing `r` route-specific functions uses O(r) space. Event transformation still costs O(k) when copying a `k`-key event.
