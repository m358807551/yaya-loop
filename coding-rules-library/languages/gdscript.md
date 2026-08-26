# GDScript best practices

> This document is imported as Part 4, programming-language practices, of `coding_rules.md`.
> Applies to: **GDScript 2.0** in Godot 4.x, with Godot 4.3 and later as the default baseline.
> This file covers GDScript language practices only. See `engine-rules.md` for Nodes, signals, Resources, and Autoloads, and the main `coding_rules.md` for general design and naming principles.

---

## 1. Static typing is the default

> This is the most important GDScript rule. Ignoring it makes a project decay dramatically faster.

GDScript is gradually typed: untyped code runs, but it gives up autocomplete, compile-time error detection, and the 28%–59% performance benefit reported by Godot's official benchmarks for typed GDScript.

### 1.1 Required rules

- **Type every variable, parameter, and return value.** Set Project Settings → Debug → GDScript → Untyped Declarations to Warning or Error.
- Use **`:=` for type inference** when the compiler can determine the right-hand type. Use an **explicit `:` annotation** when it cannot, or when the annotation clarifies intent.

```gdscript
# Prefer inference when the right-hand type is clear.
var speed := 100.0
var enemies: Array[Enemy] = []
var position := Vector2(10, 20)

# Annotate when inference is unclear or a constraint matters.
@onready var sprite: Sprite2D = $Sprite2D
var damage: int = stats.attack

# Always type complete function signatures.
func apply_damage(target: Node, amount: int) -> void:
	target.health -= amount

func find_nearest_enemy(from: Vector2) -> Enemy:
	# ...
	return null
```

### 1.2 Typed arrays and dictionaries

- **Give collections element types:** `Array[Enemy]`, `Array[int]`, and, on Godot 4.4 and later, `Dictionary[String, ItemData]`.
- Nested generics support only one typed level: `Array[Array]` is valid, but `Array[Array[int]]` is not.
- A typed array checks values at runtime when they are inserted. Treat that early failure as useful bug detection.

### 1.3 Typing is not dogma

- A short-lived local in a closure or tiny utility may use `var x = foo()` when it remains obvious.
- `Variant` is a legitimate tool for APIs such as `Dictionary.get()` and `Array.pop_back()`; do not spread it beyond the boundary that requires it.
- Remember the two behaviors of `as`:
  - A failed Object cast returns `null`: `var player := body as Player`; follow it with `if not player: return`.
  - A failed built-in type cast raises a runtime error; casting a String value with `value as int` is not safe.

---

## 2. Naming conventions

### 2.1 Identifier casing

| Construct | Style | Example |
| --- | --- | --- |
| Variables and functions | `snake_case` | `player_health`, `apply_damage()` |
| Private members and virtual callbacks | `_snake_case` | `_internal_state`, `_ready()` |
| Constants | `CONSTANT_CASE` | `MAX_HEALTH`, `DEFAULT_SPEED` |
| Enum type names | `PascalCase` | `enum Direction` |
| Enum members | `CONSTANT_CASE` | `Direction.NORTH` |
| `class_name` | `PascalCase` | `class_name PlayerStats` |
| Signals | event-oriented `snake_case`, often past tense | `health_changed`, `died`, `item_collected` |
| Signal callbacks | `_on_<signal_name>` or `_on_<source>_<signal_name>` | `_on_pressed`, `_on_player_died` |

### 2.2 Filenames and `class_name`

- A `.gd` filename must be the `snake_case` form of its `class_name`: `class_name PlayerStats` belongs in `player_stats.gd`.
- This avoids cross-platform failures between case-insensitive and case-sensitive filesystems.

### 2.3 Numeric literals

- Floats must include both leading and trailing digits: use `0.5`, not `.5`, and `2.0`, not `2.`.
- Separate large numbers with underscores: use `1_000_000`, not `1000000`.

### 2.4 Names express intent

- Do not encode the type in the name: use `health: int`, not `int_health`.
- Start Booleans with `is_`, `has_`, `can_`, or `should_`.
- Name functions with verb phrases such as `spawn_enemy` and `apply_damage`.
- Avoid abbreviations except established domain terms such as `pos`, `vel`, `hp`, `dt`, `fps`, and `xy`.

---

## 3. Official GDScript member order

Insert new members in this order; do not append unrelated declarations at the end of a file.

```gdscript
@tool
class_name PlayerController
extends CharacterBody2D

## Controls the player character.

signal health_changed(new_health: int)
signal died

enum State { IDLE, RUNNING, JUMPING }

const MAX_HEALTH := 100
const JUMP_VELOCITY := -400.0

static var instance_count: int = 0

@export var speed: float = 200.0
@export var max_jumps: int = 2

var current_health: int = MAX_HEALTH
var current_state: State = State.IDLE

var _jumps_remaining: int = 0
var _last_damage_source: Node = null

@onready var sprite: Sprite2D = $Sprite2D
@onready var hitbox: Area2D = $Hitbox

func _init() -> void:
	instance_count += 1

func _ready() -> void:
	health_changed.connect(_on_health_changed)

func _process(delta: float) -> void:
	pass

func _physics_process(delta: float) -> void:
	pass

func take_damage(amount: int) -> void:
	current_health -= amount
	health_changed.emit(current_health)

func _on_health_changed(new_value: int) -> void:
	pass
```

The order is: annotations, `class_name`, `extends`, documentation, signals, enums, constants, static variables, exported variables, public variables, private variables, `@onready` variables, `_init`, `_ready`, process callbacks, public methods, then private methods and signal callbacks. In particular, `@export` precedes ordinary variables and `@onready` follows them.

---

## 4. Indentation and formatting

- Indent with tabs, not spaces; this is the Godot editor default.
- Use LF line endings and UTF-8 without a BOM.
- End every file with one newline.
- Indent continuation lines two levels so they are visually distinct from ordinary blocks.

```gdscript
var result := some_long_function(
		first_argument,
		second_argument,
		third_argument,
)

if (some_condition_that_is_long
		and another_condition
		and yet_another_one):
	do_something()
```

---

## 5. `@export`, `@onready`, setters, and getters

### 5.1 Common export annotations

```gdscript
@export var speed: float = 100.0
@export_range(0, 100, 1) var health: int = 100
@export_range(0.0, 1.0, 0.01) var volume: float
@export_enum("Easy", "Normal", "Hard") var difficulty: int
@export_file("*.json") var config_path: String
@export_dir var save_dir: String
@export_color_no_alpha var tint: Color
@export_multiline var description: String
@export_node_path("Sprite2D") var sprite_path: NodePath
@export_group("Movement")
@export var movement_speed: float
@export var jump_height: float
@export_group("")
```

### 5.2 Godot 4 setter and getter syntax

```gdscript
var hp: int = 100:
	set(value):
		if hp != value:
			hp = value
			health_changed.emit(hp)
	get:
		return hp

var display_name: String = "":
	set(value):
		display_name = value
		_update_label()

var score: int = 0:
	set = _set_score,
	get = _get_score

func _set_score(value: int) -> void:
	score = value

func _get_score() -> int:
	return score
```

Inside a property's own inline setter or getter, directly reading or writing that property name accesses the underlying value and does not recurse. The same exception applies inside a function assigned directly as that property's setter or getter. It does not propagate into helper functions called by the setter:

```gdscript
var hp: int = 100:
	set(value):
		_assign_hp(value)

func _assign_hp(value: int) -> void:
	hp = value # Infinite recursion: this helper is not the setter itself.
```

Keep the direct assignment inside the setter, or use a backing field such as `_hp` when assignment must pass through another function.

---

## 6. Godot 4 signal syntax

### 6.1 Declaration and emission

Signal parameters should be statically typed whenever their types can be expressed.

```gdscript
signal health_changed(new_health: int, max_health: int)
signal died

health_changed.emit(current_hp, MAX_HEALTH)
died.emit()
```

Use `.emit()` in Godot 4, not the old string-based `emit_signal()` form.

### 6.2 Connections

```gdscript
button.pressed.connect(_on_button_pressed)
button.pressed.connect(_on_button_pressed.bind("attack"))
timer.timeout.connect(_on_timeout, CONNECT_ONE_SHOT)
some_signal.connect(_on_some_signal, CONNECT_DEFERRED)
button.pressed.connect(func() -> void: print("clicked"))

# Godot 3 style: do not use.
button.connect("pressed", self, "_on_button_pressed")
```

Prefer Callable connections because the editor can check the target method. Name a callback `_on_<signal_name>` for a locally observed signal and `_on_<source>_<signal_name>` when observing another object.

---

## 7. Lambdas and Callable

GDScript 2.0 supports function literals. Use a lambda for a small, temporary function and a normal function for reused behavior.

```gdscript
var sorted: Array[Enemy] = enemies.duplicate()
sorted.sort_custom(func(a: Enemy, b: Enemy) -> bool: return a.threat > b.threat)

var visible_enemies: Array[Enemy] = enemies.filter(
	func(enemy: Enemy) -> bool: return enemy.is_visible()
)
var damages: Array[int] = []
for enemy: Enemy in enemies:
	damages.append(enemy.attack)
var total: int = enemies.reduce(
	func(accumulator: int, enemy: Enemy) -> int: return accumulator + enemy.attack,
	0,
)

button.pressed.connect(func() -> void: score += 10)

var compute_damage := func compute(base: int, multiplier: float) -> int:
	return int(base * multiplier)
print(compute_damage.call(10, 1.5))
```

Name a nontrivial lambda, as in `func compute(...)`, so stack traces identify it during debugging.

### 7.1 Lambda constraints

- Invoke a lambda with `.call()`, as in `my_lambda.call(arg1, arg2)`; do not write `my_lambda(...)`.
- Closures capture values at creation time. Mutating a captured scalar changes the lambda's copy, while the contents of a captured reference type such as Array, Dictionary, or Object remain shared.

```gdscript
var counter := 0
var increment := func() -> void: counter += 1
increment.call()
print(counter) # Still 0.

var items: Array[int] = []
var add_item := func() -> void: items.append(1)
add_item.call()
print(items) # [1]
```

- A lambda cannot be `static`; use a normal static function for reusable utilities.
- Functional calls such as `filter` and `map` add Callable overhead. Prefer readability on cold paths, but use a direct `for` loop in per-frame or large-array hot paths.

---

## 8. Error handling

> GDScript has no try-catch. Do not copy exception examples from outdated or unrelated tutorials.

### 8.1 Three error signals

```gdscript
# Development invariant; assertions are ignored in non-debug builds.
func take_damage(amount: int) -> void:
	assert(amount >= 0, "damage amount must be non-negative")
	health -= amount

# Recoverable failure: report it and return a safe result.
func load_config(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		push_error("config file not found: %s" % path)
		return {}
	return {}

# Non-fatal warning.
func deprecated_function() -> void:
	push_warning("deprecated_function is deprecated; use new_function")
```

- `assert` protects conditions that must never be false during development.
- Assertions are ignored in non-debug builds, and their conditions are not evaluated in release exports. An assertion expression must never contain side effects.
- `push_error` records an error while allowing execution to continue.
- `push_warning` reports a non-fatal concern.

### 8.2 Keywords that do not exist

- There is no `throw`, `try`, `except`, or `finally` in GDScript.
- Perform lifecycle cleanup in `_exit_tree()` or `_notification(what)` where appropriate.

### 8.3 Error-handling patterns

Use one of these explicit patterns:

1. Return an error code and output data, following the style of Godot APIs.
2. Return `null` and require the caller to check it.
3. Return a result object containing success, data, and an error message.

```gdscript
var file := FileAccess.open("res://data.json", FileAccess.READ)
if not file:
	var error := FileAccess.get_open_error()
	push_error("failed to open: %s" % error)
	return

func find_enemy_by_id(id: int) -> Enemy:
	for enemy in enemies:
		if enemy.id == id:
			return enemy
	return null

class Result:
	var success: bool
	var data: Variant
	var error: String
```

### 8.4 Null and freed Objects

- Document when a typed Object return may still be `null`, and require callers to check it.
- Use `is_instance_valid(node)` before accessing an Object that may have been freed, especially after `await` or inside a coroutine.
- Use `node.is_queued_for_deletion()` to detect a Node that has received `queue_free()` but has not yet left the tree.
- Default arrays and dictionaries to empty containers rather than `null`.

---

## 9. Documentation comments

GDScript 4 uses `##` documentation comments, which the editor and documentation generator recognize.

```gdscript
## Controls the player character.
##
## Handles movement, jumping, and attacks. Input collection belongs to
## [InputHandler], not this class.
class_name PlayerController
extends CharacterBody2D

## Current health. Emits [signal died] when it reaches zero.
var current_health: int = 100

## Applies [param amount] damage from [param source].
## The amount must be non-negative. Returns the remaining health.
func take_damage(amount: int, source: Node) -> int:
	return current_health
```

- `##` is documentation; `#` is an ordinary comment.
- Documentation supports BBCode and references such as `[b]text[/b]`, `[code]value[/code]`, `[param x]`, `[signal foo]`, `[method bar]`, and `[member baz]`.
- Put class documentation after the `class_name` and `extends` declarations, following the member order above.
- Document every important public API; private `_` methods may omit documentation when their intent is obvious.

---

## 10. Control-flow conventions

### 10.1 Return placement

- Use `return` for guard clauses at the beginning of a function or for the final result.
- Avoid scattered returns in the middle of a function; keep data flow easy to follow.

```gdscript
func apply_damage(target: Node, amount: int) -> int:
	if not is_instance_valid(target):
		return 0
	if amount <= 0:
		return 0

	var actual_damage := _calculate_damage(target, amount)
	target.health -= actual_damage
	return actual_damage
```

### 10.2 Do not mutate a collection while iterating it

Mutation can skip elements or move indexes out of bounds. Build a filtered collection, iterate indexes backward, or collect removals first.

```gdscript
enemies = enemies.filter(func(enemy: Enemy) -> bool: return not enemy.is_dead)

for index in range(enemies.size() - 1, -1, -1):
	if enemies[index].is_dead:
		enemies.remove_at(index)

var to_remove: Array[Enemy] = []
for enemy in enemies:
	if enemy.is_dead:
		to_remove.append(enemy)
for enemy in to_remove:
	enemies.erase(enemy)
```

### 10.3 Conditional expressions

GDScript uses Python-style `a if condition else b`, not `condition ? a : b`.

```gdscript
var status := "alive" if hp > 0 else "dead"
var first := items[0] if not items.is_empty() else null
```

---

## 11. Packed arrays for performance-sensitive data

| Type | Typical use |
| --- | --- |
| `PackedByteArray` | File or network byte streams |
| `PackedInt32Array`, `PackedInt64Array` | Integer data |
| `PackedFloat32Array`, `PackedFloat64Array` | Floating-point data |
| `PackedStringArray` | Strings |
| `PackedVector2Array`, `PackedVector3Array` | Particle positions or path points |
| `PackedColorArray` | Colors |

Use packed arrays for tens of thousands of homogeneous values, performance-sensitive iteration, or direct serialization and transport. Prefer ordinary `Array[T]` for a few hundred values, mixed types, Object references, or frequent insertion and removal, because packed-array mutation is more expensive.

---

## 12. The `static` keyword in Godot 4

```gdscript
class_name MathUtils
extends Object

static var instance_count: int = 0

static func clamp_angle(angle: float) -> float:
	return fposmod(angle + PI, TAU) - PI

static func _static_init() -> void:
	print("MathUtils loaded")
```

- Use static functions for pure utility methods and static variables for class-wide counters.
- `_static_init()` runs once when the script is loaded.
- A static function cannot access `self` or instance members.
- A lambda cannot be static.
- Static variables disappear when the script unloads; they are not durable global state. Use an Autoload plus a Resource for data that must persist across Scenes.

---

## 13. GDScript anti-pattern checklist

- Untyped declarations: they discard static checking and typed-code performance.
- Combining `@onready` and `@export` on one variable: `@onready` overwrites the exported value during `_ready()` and Godot 4 emits `ONREADY_WITH_EXPORT`.
- Writing a property from a helper called by that property's setter: infinite recursion because the helper does not receive the setter's direct-access exception.
- Mutating a collection during iteration: skipped elements or invalid indexes.
- Calling `free()` where `queue_free()` is required by the engine lifecycle.
- String-based `emit_signal("name", args)` instead of `signal_name.emit(args)`.
- String-based `connect("signal", self, "method")` instead of `signal.connect(callable)`.
- Scattered returns in the middle of a function.
- Pervasive `Variant`: reduced static checking and performance.
- Lambdas in per-frame or other hot paths without measurement.
- Node and Object `==` compares reference identity, not value equality. Never compare or access an Object that may have been freed without first calling `is_instance_valid`.
- Using `null` instead of `[]` or `{}` as a collection default.
- Printing every frame; use a counter, a breakpoint, or targeted logging.

---

## 14. Debugging utilities

- `print()` provides basic output.
- `prints("hp:", hp, "pos:", position)` separates values with spaces.
- `printt(...)` separates values with tabs for aligned columns.
- `print_debug()` includes the filename and line number.
- A `breakpoint` statement triggers the debugger when running in the editor.
- `OS.alert("message")` displays a debugging dialog; never leave it in a release build.
- `@warning_ignore("unused_variable")` suppresses one warning temporarily. Overuse is an anti-pattern because warnings usually identify a real issue.
