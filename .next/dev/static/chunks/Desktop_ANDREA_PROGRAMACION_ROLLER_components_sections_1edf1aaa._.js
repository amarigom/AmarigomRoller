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
"use client";
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
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>QuoteForm
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
function QuoteForm() {
    _s();
    // 1. Estado para los datos del formulario
    const [formData, setFormData] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        email: "",
        color: "",
        width: "",
        height: "",
        fabric_type: "blackout",
        quality: "premium",
        observations: ""
    });
    // 2. Estados para la interfaz (mensaje y carga)
    const [enviando, setEnviando] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [message, setMessage] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        text: ""
    });
    // 3. Función para manejar el envío
    const handleSubmit = async (e)=>{
        e.preventDefault();
        setEnviando(true);
        setMessage({
            text: ""
        }); // Limpiamos mensajes anteriores
        try {
            const API_URL = "https://amarigomroller-backend-test.onrender.com/quote/request";
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            const result = await response.json();
            if (response.ok && result.success) {
                setEnviando(false);
                setMessage({
                    text: "Cotización enviada exitosamente. Nos contactaremos pronto."
                });
                // Opcional: Limpiar el formulario
                setFormData({
                    email: "",
                    color: "",
                    width: "",
                    height: "",
                    fabric_type: "blackout",
                    quality: "premium",
                    observations: ""
                });
            } else {
                throw new Error(result.error || result.message || "Error en el servidor");
            }
        } catch (error) {
            setEnviando(false);
            console.error("Error al enviar:", error);
            setMessage({
                text: "Error al enviar la solicitud. Intente nuevamente."
            });
        } finally{
            // Limpiar mensaje después de 5 segundos, pase lo que pase
            setTimeout(()=>setMessage({
                    text: ""
                }), 5000);
        }
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        className: "py-24 bg-black border-t border-white/5",
        id: "presupuesto",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "container mx-auto px-6 max-w-4xl",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "text-center mb-16",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                            className: "text-[#c9a961] text-3xl font-serif uppercase tracking-[0.3em] mb-4",
                            children: "Cotización Online"
                        }, void 0, false, {
                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                            lineNumber: 71,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "text-gray-500 italic tracking-widest text-sm",
                            children: "Ingresá las medidas de tus aberturas"
                        }, void 0, false, {
                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                            lineNumber: 74,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                    lineNumber: 70,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("form", {
                    className: "space-y-6",
                    onSubmit: handleSubmit,
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "grid grid-cols-1 md:grid-cols-2 gap-6",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                    type: "email",
                                    placeholder: "Tu Email",
                                    required: true,
                                    value: formData.email,
                                    className: "bg-zinc-900 p-3 text-white outline-none hover:scale-[1.02] hover:shadow-[0_0_15px_rgba(201,169,97,0.2)] transition-all border border-transparent focus:border-[#c9a961]/50",
                                    onChange: (e)=>setFormData({
                                            ...formData,
                                            email: e.target.value
                                        })
                                }, void 0, false, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                                    lineNumber: 81,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                    type: "text",
                                    placeholder: "Color deseado (opcional)",
                                    value: formData.color,
                                    className: "bg-zinc-900 p-3 text-white outline-none hover:scale-[1.02] hover:shadow-[0_0_15px_rgba(201,169,97,0.2)] transition-all border border-transparent focus:border-[#c9a961]/50",
                                    onChange: (e)=>setFormData({
                                            ...formData,
                                            color: e.target.value
                                        })
                                }, void 0, false, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                                    lineNumber: 89,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                            lineNumber: 80,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "grid grid-cols-2 md:grid-cols-4 gap-4",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                    type: "number",
                                    placeholder: "Ancho",
                                    value: formData.width,
                                    className: "bg-zinc-900 p-3 text-center text-white outline-none hover:scale-[1.05] transition-all",
                                    onChange: (e)=>setFormData({
                                            ...formData,
                                            width: e.target.value
                                        })
                                }, void 0, false, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                                    lineNumber: 99,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                    type: "number",
                                    placeholder: "Alto",
                                    value: formData.height,
                                    className: "bg-zinc-900 p-3 text-center text-white outline-none hover:scale-[1.05] transition-all",
                                    onChange: (e)=>setFormData({
                                            ...formData,
                                            height: e.target.value
                                        })
                                }, void 0, false, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                                    lineNumber: 106,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                    value: formData.fabric_type,
                                    className: "bg-zinc-900 p-3 text-white outline-none cursor-pointer",
                                    onChange: (e)=>setFormData({
                                            ...formData,
                                            fabric_type: e.target.value
                                        }),
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                            value: "blackout",
                                            children: "Blackout"
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                                            lineNumber: 119,
                                            columnNumber: 15
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                            value: "sunscreen",
                                            children: "Sunscreen"
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                                            lineNumber: 120,
                                            columnNumber: 15
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                            value: "tradicional",
                                            children: "Tradicional"
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                                            lineNumber: 121,
                                            columnNumber: 15
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                                    lineNumber: 114,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                    value: formData.quality,
                                    className: "bg-zinc-900 p-3 text-white outline-none cursor-pointer",
                                    onChange: (e)=>setFormData({
                                            ...formData,
                                            quality: e.target.value
                                        }),
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                            value: "premium",
                                            children: "Premium"
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                                            lineNumber: 129,
                                            columnNumber: 15
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                            value: "estandar",
                                            children: "Estandar"
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                                            lineNumber: 130,
                                            columnNumber: 15
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                            value: "superior",
                                            children: "Superior"
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                                            lineNumber: 131,
                                            columnNumber: 15
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                                    lineNumber: 124,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                            lineNumber: 98,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("textarea", {
                            placeholder: "Observaciones",
                            value: formData.observations,
                            className: "w-full bg-zinc-900 p-3 h-24 text-white outline-none hover:border-[#c9a961]/30 border border-transparent transition-all",
                            onChange: (e)=>setFormData({
                                    ...formData,
                                    observations: e.target.value
                                })
                        }, void 0, false, {
                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                            lineNumber: 135,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "h-4 text-center",
                            children: message.text && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "text-[#f5f5dc] text-xs uppercase tracking-[0.2em] animate-pulse",
                                children: message.text
                            }, void 0, false, {
                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                                lineNumber: 144,
                                columnNumber: 15
                            }, this)
                        }, void 0, false, {
                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                            lineNumber: 142,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            type: "submit",
                            disabled: enviando,
                            className: `
              w-full py-4 uppercase tracking-[0.5em] text-[10px] font-bold
              transition-all duration-500 border
              ${enviando ? 'bg-zinc-800 border-zinc-700 text-zinc-500 cursor-not-allowed' : 'bg-transparent border-[#c9a961] text-[#c9a961] hover:bg-[#c9a961] hover:text-black hover:shadow-[0_0_30px_rgba(201,169,97,0.4)]'}
            `,
                            children: enviando ? 'Procesando...' : 'Solicitar Presupuesto'
                        }, void 0, false, {
                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                            lineNumber: 150,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
                    lineNumber: 79,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
            lineNumber: 69,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/QuoteForm.tsx",
        lineNumber: 68,
        columnNumber: 5
    }, this);
}
_s(QuoteForm, "bPSP1ofjjA+/OxSmNxrfgXgK4sQ=");
_c = QuoteForm;
var _c;
__turbopack_context__.k.register(_c, "QuoteForm");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>Promotions
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$image$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/image.js [app-client] (ecmascript)");
"use client";
;
;
const promotions = [
    {
        id: 101,
        badge: "-25%",
        title: {
            es: "Cortinas tradicionales Blackout y voile texturado o gasa",
            en: "Sunscreen Combo"
        },
        description: {
            es: "Cortinas de 2 paños. Cada paño de 1,5 m de ancho x 2,10 m de alto",
            en: "2 traditional blinds blinds up to 1.5m x 2,1m"
        },
        oldPrice: "$305.000",
        newPrice: "$260.000",
        image: "/images/products/sunscreen.jpg"
    },
    {
        id: 102,
        badge: "-30%",
        title: {
            es: "Roller Blackout Premium y Sunscreen",
            en: "Roller Blackout Premium and Sunscreen"
        },
        description: {
            es: "Cortina blackout premium 1,5 m x 1,5 m + cortina sunscreen 1,5 m x 1,5 m",
            en: "Premium blackout blind with installation included"
        },
        oldPrice: "$350.000",
        newPrice: "$245.000",
        image: "/images/products/blackout.jpg"
    }
];
function Promotions({ lang = "es" }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        className: "py-16 bg-background",
        id: "promotions",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "container mx-auto px-4",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "bg-primary text-primary-foreground text-center py-4 mb-12 rounded-lg font-bold text-xl tracking-wide uppercase",
                    children: lang === "es" ? "PROMOCIONES ESPECIALES" : "SPECIAL OFFERS"
                }, void 0, false, {
                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
                    lineNumber: 36,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "grid md:grid-cols-2 gap-8 max-w-5xl mx-auto",
                    children: promotions.map((promo)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "group relative border border-border rounded-xl overflow-hidden bg-card hover:shadow-xl transition-all duration-300",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "absolute top-4 left-4 z-10 bg-destructive text-white px-3 py-1 rounded-full text-sm font-bold",
                                    children: promo.badge
                                }, void 0, false, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
                                    lineNumber: 50,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "relative h-64 w-full overflow-hidden",
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$image$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                        src: promo.image,
                                        alt: promo.title[lang],
                                        fill: true,
                                        className: "object-cover transition-transform duration-500 group-hover:scale-110"
                                    }, void 0, false, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
                                        lineNumber: 56,
                                        columnNumber: 17
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
                                    lineNumber: 55,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "p-6",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                            className: "text-2xl font-serif font-semibold mb-2 text-foreground",
                                            children: promo.title[lang]
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
                                            lineNumber: 66,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                            className: "text-muted-foreground mb-4 h-12",
                                            children: promo.description[lang]
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
                                            lineNumber: 69,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "flex items-center gap-4 mb-6",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    className: "text-muted-foreground line-through text-lg",
                                                    children: promo.oldPrice
                                                }, void 0, false, {
                                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
                                                    lineNumber: 74,
                                                    columnNumber: 19
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    className: "text-2xl font-bold text-primary",
                                                    children: promo.newPrice
                                                }, void 0, false, {
                                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
                                                    lineNumber: 77,
                                                    columnNumber: 19
                                                }, this)
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
                                            lineNumber: 73,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            className: "w-full bg-primary text-primary-foreground py-3 rounded-md font-medium hover:opacity-90 transition-opacity",
                                            onClick: ()=>console.log("Contactar por whatsapp:", promo.id),
                                            children: lang === "es" ? "Contactar por Whatsapp" : "Consult"
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
                                            lineNumber: 82,
                                            columnNumber: 17
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
                                    lineNumber: 65,
                                    columnNumber: 15
                                }, this)
                            ]
                        }, promo.id, true, {
                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
                            lineNumber: 45,
                            columnNumber: 13
                        }, this))
                }, void 0, false, {
                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
                    lineNumber: 43,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
            lineNumber: 34,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/sections/Promotions.tsx",
        lineNumber: 33,
        columnNumber: 5
    }, this);
}
_c = Promotions;
var _c;
__turbopack_context__.k.register(_c, "Promotions");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=Desktop_ANDREA_PROGRAMACION_ROLLER_components_sections_1edf1aaa._.js.map