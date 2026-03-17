(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>Gallery
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client"; // <--- ¡ESTO ES VITAL! Sin esto, el carrusel no se mueve.
;
function Gallery() {
    _s();
    // 1. Definimos las imágenes 
    const galleryImages = [
        "/images/gallery/img1.jpg",
        "/images/gallery/img2.jpg",
        "/images/gallery/img3.jpg",
        "/images/gallery/img4.jpg",
        "/images/gallery/img5.jpg",
        "/images/gallery/img6.jpg",
        "/images/gallery/img7.jpg",
        "/images/gallery/img8.jpg",
        "/images/gallery/img9.jpg",
        "/images/gallery/img10.jpg"
    ];
    // 2. Lógica del carrusel
    const [currentIndex, setCurrentIndex] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(0);
    const nextSlide = ()=>{
        setCurrentIndex((prev)=>prev === galleryImages.length - 1 ? 0 : prev + 1);
    };
    const prevSlide = ()=>{
        setCurrentIndex((prev)=>prev === 0 ? galleryImages.length - 1 : prev - 1);
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        className: "py-24 bg-[#0a0a0a]",
        id: "gallery",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "container mx-auto px-6",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                    className: "text-3xl font-serif text-[#c9a961] mb-12 text-center tracking-widest uppercase",
                    children: "Galería de Instalaciones"
                }, void 0, false, {
                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
                    lineNumber: 35,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "relative group max-w-5xl mx-auto overflow-hidden",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex transition-transform duration-700 ease-in-out",
                            style: {
                                transform: `translateX(-${currentIndex * 100}%)`
                            },
                            children: galleryImages.map((src, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "min-w-full h-[500px] px-2",
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("img", {
                                        src: src,
                                        alt: `Instalación ${index + 1}`,
                                        className: "w-full h-full object-cover rounded-sm border border-white/5"
                                    }, void 0, false, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
                                        lineNumber: 47,
                                        columnNumber: 17
                                    }, this)
                                }, index, false, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
                                    lineNumber: 46,
                                    columnNumber: 15
                                }, this))
                        }, void 0, false, {
                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
                            lineNumber: 41,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: prevSlide,
                            className: "absolute left-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-[#c9a961] text-white hover:text-black p-3 transition-all rounded-full z-20",
                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
                                width: "24",
                                height: "24",
                                viewBox: "0 0 24 24",
                                fill: "none",
                                stroke: "currentColor",
                                strokeWidth: "2",
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("polyline", {
                                    points: "15 18 9 12 15 6"
                                }, void 0, false, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
                                    lineNumber: 62,
                                    columnNumber: 15
                                }, this)
                            }, void 0, false, {
                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
                                lineNumber: 61,
                                columnNumber: 13
                            }, this)
                        }, void 0, false, {
                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
                            lineNumber: 57,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: nextSlide,
                            className: "absolute right-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-[#c9a961] text-white hover:text-black p-3 transition-all rounded-full z-20",
                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
                                width: "24",
                                height: "24",
                                viewBox: "0 0 24 24",
                                fill: "none",
                                stroke: "currentColor",
                                strokeWidth: "2",
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("polyline", {
                                    points: "9 18 15 12 9 6"
                                }, void 0, false, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
                                    lineNumber: 72,
                                    columnNumber: 15
                                }, this)
                            }, void 0, false, {
                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
                                lineNumber: 71,
                                columnNumber: 13
                            }, this)
                        }, void 0, false, {
                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
                            lineNumber: 67,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "flex justify-center gap-2 mt-8",
                            children: galleryImages.map((_, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                    onClick: ()=>setCurrentIndex(index),
                                    className: `h-1 transition-all duration-300 ${currentIndex === index ? "w-8 bg-[#c9a961]" : "w-2 bg-zinc-700"}`
                                }, index, false, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
                                    lineNumber: 79,
                                    columnNumber: 15
                                }, this))
                        }, void 0, false, {
                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
                            lineNumber: 77,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
                    lineNumber: 39,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
            lineNumber: 34,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Gallery.tsx",
        lineNumber: 33,
        columnNumber: 5
    }, this);
}
_s(Gallery, "tusBbsahUVevXfyh6oH5R6YDC9Q=");
_c = Gallery;
var _c;
__turbopack_context__.k.register(_c, "Gallery");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=Desktop_ANDREA_PROGRAMACION_ROLLER_components_sections_Gallery_tsx_54e32565._.js.map