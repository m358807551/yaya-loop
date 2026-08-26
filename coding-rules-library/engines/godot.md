# Godot best practices

> This file is imported as Layer 3, engine practices, of `coding_rules.md`.
> **Supported version:** Godot 4.3 and later; most guidance applies to Godot 4.x.
> This file covers Godot-specific behavior and does not repeat general principles from the main Coding Rules.

---

## 1. Core model: scenes are reusable objects

In Godot, a Scene is not merely a level. It is a reusable composition of nodes. A button, enemy, HUD, and level can each be a Scene.

- Give every sufficiently independent unit its own Scene: characters, enemies, projectiles, UI panels, and pickups.
- A Scene should run independently through Play Current Scene. Failure outside its parent context indicates excessive external dependency.
- Organize the Scene tree by logical ownership rather than incidental spatial proximity. A player need not be a child of `Room` merely because the player is currently inside it.

---

## 2. Node communication

> Communication structure is one of the most common sources of long-term coupling in Godot projects.

### 2.1 Golden rule: call down, signal up

- **Call down:** A parent may call a child through `get_node()` or `$NodePath`.
- **Signal up:** A child reports events to parents or peers through signals, not `get_parent()`.
- **Communicate across siblings through their common parent:** the child emits, and the parent coordinates the sibling.

### 2.2 Prohibited tree-path coupling

Do not write paths such as:

```gdscript
# All of these are anti-patterns.
get_node("../../SomeNode/SomeOtherNode")
get_parent().get_parent().get_node("SomeNode")
get_tree().get_root().get_node("SomeNode/SomeOtherNode")
```

A small Scene-tree change breaks these paths. A node that requires a particular chain of parents cannot run independently or be reused safely.

### 2.3 Signals

- Declare a custom signal with `signal` and emit it with `signal_name.emit(args)`, using Godot 4 syntax.
- Prefer editor connections for nodes that already exist in a Scene. Connect runtime-instantiated nodes in code.
- Connect through `Callable`, such as `button.pressed.connect(_on_pressed)`, rather than a string method name so the editor can check the target.
- Name signals as past events or changed state: `health_changed`, `died`, or `item_collected`, not imperative names such as `change_health`.
- Return after emission when appropriate and do not assume what a receiver did. A sender must not depend on whether anyone listened.

### 2.4 Event bus for distant communication

When forwarding signals through several Scene levels becomes a signal maze, use a focused autoload event bus:

```gdscript
# Events.gd, registered as an autoload
extends Node

signal player_died
signal score_changed(new_score: int)
signal level_completed(level_id: String)
```

Any node may call `Events.player_died.emit()` or connect with `Events.score_changed.connect(_on_score_changed)`.

Use the bus sparingly:

- Do not route nearby communication inside one Scene through the bus.
- Use it for cross-Scene, cross-module, or otherwise impractically long communication paths.
- Group bus signals by domain. Do not let one event-bus script become a God Object.

---

## 3. Autoload conventions

### 3.1 Appropriate Autoload uses

- data that persists across Scene changes, such as save data, settings, or current progression
- global services such as audio, Scene transitions, localization, or input mapping
- a focused event bus
- read-mostly global configuration such as game constants or difficulty values

### 3.2 Inappropriate Autoload uses

- state used only inside one Scene
- convenience-only global access when an `@export` reference or shared Resource provides an explicit dependency
- domain behavior that makes the autoload grow into a God Object

### 3.3 Autoload implementation

- Use PascalCase names such as `PlayerData`, `AudioManager`, and `Events`; they become global identifiers.
- Keep Autoload nodes free of presentation. They should expose data, signals, and focused public methods rather than render nodes.
- Prefer read-heavy interfaces. Frequent external field mutation increases coupling; expose queries and meaningful commands or signals instead.

---

## 4. Resource: the core data-driven tool

Godot's `Resource` is comparable to Unity's ScriptableObject and should be used deliberately.

### 4.1 When to use Resource

- static definitions such as items, skills, enemy parameters, level configuration, and dialogue
- typed, Inspector-editable configuration that may reference other Resources or Textures
- shared data referenced by several nodes, for example `@export var data: PlayerStats`

### 4.2 Custom Resource shape

```gdscript
# res://resources/enemy_stats.gd
class_name EnemyStats
extends Resource

@export var enemy_name: String = ""
@export var max_health: int = 100
@export var attack: int = 10
@export var icon: Texture2D
@export var loot_table: Array[ItemData] = []
```

Create an `EnemyStats` `.tres` through FileSystem → New → Resource, then edit it in the Inspector.

### 4.3 Resource traps

1. **One `.tres` file is one shared in-memory Resource.** Mutating it through one node affects every node referencing it.
   - For an independent instance, enable Local to Scene in the Resource Inspector or call `stats = stats.duplicate()`.
2. **Prefer `.tres` during development.** It is text, reviewable in Git, and diffable. Consider binary `.res` only for release or genuinely large resource data.
3. **Runtime writes belong under `user://`, not `res://`.** For example, use `ResourceSaver.save(res, "user://save.tres")`.
4. **A Resource has no `_process`.** It is data and does not participate in the Scene tree.
5. **A custom Resource does not automatically emit `changed`.** Call `emit_changed()` from a setter:

   ```gdscript
   @export var hp: int:
       set(value):
           if hp != value:
               hp = value
               emit_changed()
   ```

### 4.4 Typical data-driven flow

1. Define structures such as `ItemData` and `SkillData` with Resource scripts.
2. Create one `.tres` file per configured item or skill.
3. Load it at runtime with `load("res://items/sword.tres")` or assign it through `@export`.
4. Change values in the Inspector without changing code.

---

## 5. Correct use of `@export` and `@onready`

### 5.1 `@export`: designer-adjustable values and references

- Expose parameters a designer should adjust, such as speed, health, cooldown, or level duration.
- Write explicit types: `@export var speed: float = 100.0`.
- Export node references such as `@export var target: Node2D` instead of depending on paths such as `../../Target`.
- Use Inspector-aware modifiers when appropriate: `@export_range(0, 100)`, `@export_file("*.json")`, `@export_color_no_alpha`, and `@export_enum("Easy", "Normal", "Hard")`.

### 5.2 `@onready`: values resolved after the Scene tree is ready

- Use it primarily for child-node references, such as `@onready var sprite: Sprite2D = $Sprite2D`.
- Never combine `@export` and `@onready` on one variable. `@onready` overwrites the value loaded from the Scene during `_ready()`, and Godot 4 warns about the combination.
- Give `@onready` variables explicit types for editor completion and checking.

### 5.3 Recommended GDScript member order

```text
1. @tool
2. class_name
3. extends
4. Documentation comments, when needed
5. signals
6. enums
7. constants
8. @export variables
9. public variables
10. private variables prefixed with _
11. @onready variables
12. _init, _ready, _process, and _physics_process
13. other public methods
14. private methods
```

---

## 6. Lifecycle and frames

### 6.1 Callback roles

| Callback | Timing | Intended use |
| --- | --- | --- |
| `_init()` | Object creation, before the Scene tree exists | Internal state independent of the Scene tree |
| `_enter_tree()` | Node enters the Scene tree | Registration with external systems |
| `_ready()` | Node and all children have entered the tree | Child references and signal connections |
| `_process(delta)` | Every rendered frame | Animation and UI updates |
| `_physics_process(delta)` | Every fixed physics frame, 60 Hz by default | Movement, collision, and AI |
| `_exit_tree()` | Node leaves the Scene tree | Deregistration and cleanup |

### 6.2 Lifecycle rules

- Put physics, movement, and collision in `_physics_process` for fixed-step reproducibility.
- Put presentation and UI work in `_process` and use `delta` for interpolation.
- Remove empty `_process` or `_physics_process` callbacks. Even empty enabled callbacks run every frame; disable them explicitly with `set_process(false)` or `set_physics_process(false)` when needed.
- `_ready()` runs the first time a node enters the Scene tree. `add_child()` triggers it; reparenting an already-ready node does not run it again.
- Do not access `$Child` in `_init()` because child nodes do not exist yet.

### 6.3 `await` and coroutines

- `await signal_name` and `await get_tree().create_timer(1.0).timeout` suspend the current function until the signal fires.
- A node may be destroyed while a coroutine is suspended. After resuming, check `is_instance_valid(self)` or `is_queued_for_deletion()` before using it.
- `queue_free()` may still allow a coroutine to resume on a later frame; code must handle that lifetime boundary.

---

## 7. Scene changes and node lifetime

### 7.1 Changing Scenes

- `get_tree().change_scene_to_file("res://levels/level2.tscn")` replaces the main Scene and destroys every node in the old Scene except Autoloads.
- `change_scene_to_packed(packed_scene)` uses a preloaded PackedScene and avoids runtime I/O at the transition.
- For large Scenes, use `preload("res://levels/big_level.tscn")` or `ResourceLoader.load_threaded_request()`.

### 7.2 Creating and destroying nodes

- Instantiate with `var enemy = enemy_scene.instantiate(); add_child(enemy)`. Godot 4 uses `instantiate()`, not Godot 3's `instance()`.
- Destroy with `queue_free()`, not `free()`. Deferred destruction avoids deleting a node while collections or callbacks are being traversed.
- Use `is_instance_valid(node)` when a reference may outlive the node, especially after asynchronous work resumes.

---

## 8. Godot-specific performance

- Node instantiation has a cost. Pool objects created hundreds of times per second, such as projectiles, particles, or damage numbers.
- For pooled nodes:
  - use `hide()`, `set_process(false)`, and `set_physics_process(false)`; remove them from the tree when that matches the pool design
  - do not use `set_deferred("process_mode", ...)` as the primary deactivation mechanism; it is a known performance trap
  - do not leave pooled objects in inherited processing mode while expecting them to consume no CPU
- Use `MultiMeshInstance2D`, `MultiMeshInstance3D`, or RenderingServer APIs for very large numbers of homogeneous objects.
- Avoid per-frame string concatenation in hot paths.
- Cache repeated `get_node()` lookups in `@onready` variables rather than resolving the same path every frame.
- Rising Orphan Nodes in Debugger → Monitors indicates nodes removed from the tree without being freed.

---

## 9. Editor conventions

### 9.1 File organization

- Organize by feature or Scene. Keep `player.tscn`, `player.gd`, `player.png`, and `player_walk.tres` together under an area such as `scenes/player/` rather than separating every file type.
- Put third-party assets under `addons/` and retain their licenses.
- Add an empty `.gdignore` to directories that should not be imported or displayed by Godot.
- Folder colors may distinguish core modules, addons, and temporary areas.

### 9.2 Godot naming

- Use `snake_case` for Scene files, script files, and directories: `player_controller.gd` and `enemy_data.tres`.
- Use `PascalCase` for C# files because filenames must match class names.
- Use `PascalCase` for node names inside Scenes, such as `PlayerSprite` and `HealthBar`.
- Use `PascalCase` for GDScript `class_name`, such as `PlayerStats`.
- Prefix Scene-specific subresources by owner, such as `player_idle.tres` and `player_run.tres`.

### 9.3 Static types and warnings

- In Godot 4.2 and later, enable the Untyped Declarations warning under Project Settings → Debug → GDScript so variables and function returns require types.
- Use `:=` for concise inference, such as `var enemies := []` and `var speed := 100.0`.
- Before deleting a resource, use FileSystem → View Owners to find references and avoid broken dependencies.

---

## 10. Editor and code signal connections

| Connection style | Use it for |
| --- | --- |
| Editor panel | Connections between nodes that already exist in one Scene |
| Code `connect()` | Runtime-instantiated nodes |

- Editor connections are visible in `.tscn` and Git diffs, but method-name refactors can be harder to trace across files.
- Code connections centralize dependencies in `_ready()`, but they are not visible when inspecting the Scene file.
- Keep one project convention. By default, use editor connections for static nodes inside one Scene and code for cross-Scene or dynamically instantiated nodes.

---

## 11. Godot anti-pattern checklist

- `get_parent()` or `get_node("../X")` for upward communication
- `$Child` access inside `_init()`
- `@export` and `@onready` on the same variable
- empty `_process` or `_physics_process` callbacks
- repeated `get_node()` calls every frame
- `free()` where `queue_free()` is required
- assuming each node has a private copy of a shared Resource
- an ever-growing Autoload that becomes a God Object
- `find_child()` or `get_tree().get_nodes_in_group()` in a hot path without caching
- imperative signal names such as `set_health` instead of event names such as `health_changed`

---

## 12. Debugging and verification tools

- **Debugger → Profiler:** measure suspected performance problems before optimizing.
- **Debugger → Monitors:** inspect FPS, Process Time, Draw Calls, Node Count, and Orphan Nodes. Continuously rising Node Count can indicate a leak.
- **Remote Scene tree:** inspect the actual runtime tree rather than assuming it matches the editor view.
- **Play Current Scene, F6:** verify Scene independence. A Scene that cannot run alone likely has excessive external dependencies.
