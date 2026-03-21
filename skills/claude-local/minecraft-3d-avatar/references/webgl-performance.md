# WebGL Performance & Context Management

## The Problem

Browsers limit simultaneous WebGL contexts to ~8-16. A shop page showing 20 items with individual `<Canvas>` will crash — early contexts get silently evicted (shows as broken/blank).

## Solution: IntersectionObserver Lazy Loading

Only mount Canvas when the element is in/near the viewport. Unmount when scrolled away.

```tsx
"use client";
import dynamic from "next/dynamic";
import React, { useRef, useState, useEffect, Suspense } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Environment } from "@react-three/drei";

function ItemPreview3DInner({ meshId, slot, fallbackEmoji, autoRotate, className }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => setIsVisible(entry.isIntersecting),
      { rootMargin: "200px" } // pre-load slightly before visible
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  const def = lookupRegistry(meshId, slot);
  if (!def) return <EmojiFallback emoji={fallbackEmoji} />;

  const Component = def.component;

  return (
    <div ref={containerRef} className={className}>
      {isVisible ? (
        <Canvas
          frameloop={autoRotate ? "always" : "demand"}
          gl={{ antialias: true, alpha: true }}
          camera={{ position: [0, 0, 1.5], fov: 50 }}
        >
          <ambientLight intensity={0.6} />
          <directionalLight position={[5, 10, 5]} intensity={0.8} />
          <Environment preset="studio" frames={1} />
          <Suspense fallback={null}>
            <RotatingGroup autoRotate={autoRotate}>
              <Component />
            </RotatingGroup>
          </Suspense>
        </Canvas>
      ) : (
        <PlaceholderFallback emoji={fallbackEmoji} />
      )}
    </div>
  );
}

// SSR-safe export
export default dynamic(() => Promise.resolve(ItemPreview3DInner), { ssr: false });
```

## Key Performance Rules

1. **`frameloop="demand"`** for static previews — only re-renders when state changes
2. **`frameloop="always"`** only for auto-rotating items
3. **`<Environment frames={1}>`** — bake environment map once, don't re-render every frame
4. **`dynamic(() => ..., { ssr: false })`** — Three.js cannot server-render
5. **WebGLErrorBoundary** — catch context creation failures and show 2D fallback
6. **`NearestFilter`** on skin textures — preserves pixel art crispness

## drei View (Future Optimization)

If `@react-three/drei` supports `<View>`, use a single shared Canvas:

```tsx
// SharedCanvasProvider wraps the page with ONE Canvas
<Canvas>
  <View.Port />
</Canvas>

// Each item uses <View> to define a viewport
<View className="w-20 h-20">
  <Component />
</View>
```

This eliminates the WebGL context limit entirely. Check `drei` version for `View` support before implementing.
