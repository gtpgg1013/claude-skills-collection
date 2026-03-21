# Architecture Reference

## File Structure

```
src/components/avatar/
├── block-character.tsx          # Main character with UV-mapped skin + accessory slots
├── avatar-canvas-3d.tsx         # Canvas wrapper with camera, lighting, orbit controls
├── avatar-editor.tsx            # Equipment selection UI
├── item-preview-3d.tsx          # Lazy 3D item preview (IntersectionObserver)
├── shared-canvas-provider.tsx   # Context wrapper (for future drei View support)
└── accessories/
    ├── accessory-registry.ts    # meshId → AccessoryDef mapping
    ├── background-registry.ts   # meshId → BackgroundDef mapping
    ├── hat-meshes.tsx           # Hat BoxGeometry components
    ├── glasses-meshes.tsx       # Glasses BoxGeometry components
    ├── weapon-meshes.tsx        # Weapon BoxGeometry components
    ├── badge-meshes.tsx         # Badge BoxGeometry components
    └── background-meshes.tsx    # Background scene compositions
```

## Registry Pattern

### AccessoryDef (body-attached items)

```typescript
export type AccessorySlot = "hat" | "glasses" | "weapon" | "badge";
export type AttachPoint = "head" | "body" | "rightArm" | "leftArm";

export interface AccessoryDef {
  meshId: string;
  slot: AccessorySlot;
  component: React.ComponentType;
  attachTo: AttachPoint;
  localPosition: [number, number, number];
  localRotation: [number, number, number];
  localScale: [number, number, number];
}

export const ACCESSORY_REGISTRY: Record<string, AccessoryDef> = {
  crown: {
    meshId: "crown",
    slot: "hat",
    component: CrownMesh,
    attachTo: "head",
    localPosition: [0, 0.50, 0],
    localRotation: [0, 0, 0],
    localScale: [1.25, 1.25, 1.25],
  },
  // ...
};
```

### BackgroundDef (scene-level, no attachment)

```typescript
export interface BackgroundDef {
  meshId: string;
  component: React.ComponentType;
}

export const BACKGROUND_REGISTRY: Record<string, BackgroundDef> = {
  bgJungle: { meshId: "bgJungle", component: BgJungle },
  // ...
};
```

### Lookup in preview component

```typescript
const def = slot === "background"
  ? getBackground(meshId)
  : getAccessory(meshId);
```

## BlockCharacter Dimensions (scale=1, U=0.1)

| Part      | Size (world units) | Center Position      |
|-----------|-------------------|---------------------|
| Head      | 0.8 × 0.8 × 0.8  | [0, 1.6, 0]        |
| Body      | 0.8 × 1.2 × 0.4  | [0, 0.6, 0]        |
| Right Arm | 0.4 × 1.2 × 0.4  | [-0.6, 0.6, 0]     |
| Left Arm  | 0.4 × 1.2 × 0.4  | [0.6, 0.6, 0]      |
| Right Leg | 0.4 × 1.2 × 0.4  | [-0.2, -0.6, 0]    |
| Left Leg  | 0.4 × 1.2 × 0.4  | [0.2, -0.6, 0]     |

**Key surfaces for attachment:**
- Head top: local y = +0.4
- Face front: local z = +0.4
- Eye level: local y ≈ +0.05
- Body front: local z = +0.2
- Arm hand area: local y ≈ -0.5

## Camera & Lighting Setup

```tsx
// Profile/editor view — shows full character with hat + background
<Canvas camera={{ position: [0, 1.0, 5.5], fov: 45 }}>
  <ambientLight intensity={0.6} />
  <directionalLight position={[5, 10, 5]} intensity={0.8} />
  <directionalLight position={[-5, 5, -5]} intensity={0.4} />
  <directionalLight position={[0, -5, 5]} intensity={0.2} />
  <Environment preset="studio" frames={1} />
</Canvas>

// Item preview — close-up on single item
<Canvas camera={{ position: [0, 0, 1.5], fov: 50 }}>
  {/* Same lighting */}
</Canvas>
```
