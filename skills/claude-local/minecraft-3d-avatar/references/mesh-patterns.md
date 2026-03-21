# Mesh Component Patterns

## Basic Item Template

```tsx
"use client";
import React from "react";

export function MyItemMesh() {
  return (
    <group>
      {/* Main body */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[width, height, depth]} />
        <meshLambertMaterial color="#HEXCOLOR" />
      </mesh>
      {/* Detail blocks */}
      <mesh position={[x, y, z]}>
        <boxGeometry args={[w, h, d]} />
        <meshLambertMaterial color="#HEXCOLOR" />
      </mesh>
    </group>
  );
}
```

## Material Selection

### meshLambertMaterial (default)
For organic, plastic, fabric items. No environment map needed.

```tsx
<meshLambertMaterial color="#FF6B35" />
```

### meshStandardMaterial (metallic items)
For metal, gold, chrome items. REQUIRES `<Environment>` for reflections.

```tsx
<meshStandardMaterial color="#FFD700" metalness={0.8} roughness={0.2} />
```

### Emissive glow (legendary/special items)
For glowing elements like gems, energy cells, fuses.

```tsx
<meshStandardMaterial
  color="#FF0000"
  emissive="#AA0000"
  emissiveIntensity={0.4}
  roughness={0.1}
/>
```

Also works on meshLambertMaterial:
```tsx
<meshLambertMaterial color="#FFD700" emissive="#FFAA00" emissiveIntensity={1.2} />
```

## Transform Guidelines

### Hats (attachTo: "head")
- Y position: 0.48-0.55 (hat bottom should be at or slightly below head top y=0.4)
- Scale: 1.2-1.3x for visual impact
- Items with variable height need individual Y tuning

### Glasses (attachTo: "head")
- Y position: ~0.05 (eye level, slightly above head center)
- Z position: ~0.42 (just in front of face surface at z=0.4)
- Scale: 1.2x

### Weapons (attachTo: "rightArm")
- X position: ~-0.25 (just outside arm outer edge)
- Y position: -0.45 to -0.52 (hand area, arm bottom at -0.6)
- Z position: ~0.1 (slightly forward)
- Rotate guns -90° around Y to point forward: `localRotation: [0, -1.57, 0]`
- Scale: 1.15-1.25x

### Badges (attachTo: "body")
- Position: [0.12, 0.2, 0.21] (upper-right chest, z=body front+0.01)
- Scale: 1.3x (badges are small, need extra scaling)

### Backgrounds (separate registry, self-positioned)
- Position inside mesh component: `<group position={[0, 0, -2]}>` (behind character)
- Width: ~3-4 units wide to frame the character
- No transforms in registry — backgrounds position themselves

## Example: Complete Hat Mesh

```tsx
// CrownMesh - golden crown with metalness + gem accents
export function CrownMesh() {
  return (
    <group>
      {/* Base band — gold metallic */}
      <mesh position={[0, -0.05, 0]}>
        <boxGeometry args={[0.52, 0.12, 0.52]} />
        <meshStandardMaterial color="#FFD700" metalness={0.8} roughness={0.2} />
      </mesh>
      {/* Center point */}
      <mesh position={[0, 0.12, 0]}>
        <boxGeometry args={[0.1, 0.2, 0.1]} />
        <meshStandardMaterial color="#FFD700" metalness={0.8} roughness={0.2} />
      </mesh>
      {/* Gem — red (front) */}
      <mesh position={[0, 0, 0.27]}>
        <boxGeometry args={[0.08, 0.08, 0.04]} />
        <meshStandardMaterial color="#FF0000" emissive="#AA0000" emissiveIntensity={0.4} roughness={0.1} />
      </mesh>
    </group>
  );
}
```

## Example: Background Scene

```tsx
export function BgJungle() {
  return (
    <group position={[0, 0, -2]}>
      {/* Ground */}
      <mesh position={[0, -1.2, 0]}>
        <boxGeometry args={[4, 0.3, 1]} />
        <meshLambertMaterial color="#2E7D32" />
      </mesh>
      {/* Tree trunk */}
      <mesh position={[-1.2, -0.2, 0]}>
        <boxGeometry args={[0.3, 1.6, 0.3]} />
        <meshLambertMaterial color="#5D4037" />
      </mesh>
      {/* Tree leaves */}
      <mesh position={[-1.2, 0.8, 0]}>
        <boxGeometry args={[1.0, 0.8, 0.8]} />
        <meshLambertMaterial color="#1B5E20" />
      </mesh>
    </group>
  );
}
```
