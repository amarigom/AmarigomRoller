module.exports = [
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/layout.tsx [app-rsc] (ecmascript, Next.js Server Component)", ((__turbopack_context__) => {

__turbopack_context__.n(__turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/layout.tsx [app-rsc] (ecmascript)"));
}),
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>CategoryPage
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-jsx-dev-runtime.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/dist/client/app-dir/link.react-server.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$api$2f$navigation$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$locals$3e$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/dist/api/navigation.react-server.js [app-rsc] (ecmascript) <locals>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$client$2f$components$2f$navigation$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/dist/client/components/navigation.react-server.js [app-rsc] (ecmascript)");
;
;
;
const productDetails = {
    blackout: {
        title: "Cortinas Blackout",
        items: [
            {
                name: "Blackout Base",
                desc: "Vinílico tricapa, bloqueo 100% luz y aislante térmico."
            },
            {
                name: "Blackout Premium",
                desc: "Textura textil elegante con la misma capacidad de bloqueo."
            }
        ]
    },
    tradicional: {
        title: "Cortinas Tradicionales",
        items: [
            {
                name: "Con Visillo",
                desc: "Doble cortina para privacidad y luz suave."
            },
            {
                name: "Con Barral o Riel",
                desc: "Sistemas clásicos reforzados."
            },
            {
                name: "Cortinas Romanas",
                desc: "Plegado horizontal estético y funcional."
            }
        ]
    },
    sunscreen: {
        title: "Cortinas Sunscreen",
        items: [
            {
                name: "Sunscreen 5%",
                desc: "Equilibrio perfecto entre visión al exterior y privacidad."
            },
            {
                name: "Sunscreen 1%",
                desc: "Trama más cerrada para mayor protección solar y térmica."
            }
        ]
    }
};
async function CategoryPage({ params }) {
    const resolvedParams = await params;
    const slug = resolvedParams.categorie;
    const category = productDetails[slug];
    if (!category) return (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$client$2f$components$2f$navigation$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["notFound"])();
    const getWhatsAppLink = (itemName)=>{
        const phone = "5492494630750";
        const message = encodeURIComponent(`Hola Andrea! Vi en la web la cortina *${itemName}* y quería pedirte un presupuesto.`);
        return `https://wa.me/${phone}?text=${message}`;
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("main", {
        className: "bg-black min-h-screen text-[#f5f5f5] p-6 md:p-12",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "max-w-5xl mx-auto",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
                    href: "/",
                    className: "text-[#f5f5f5]/50 hover:text-[#c9a961] mb-12 inline-block transition-colors uppercase tracking-[0.2em] text-xs",
                    children: "← Volver al Inicio"
                }, void 0, false, {
                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx",
                    lineNumber: 52,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                    className: "text-4xl md:text-5xl font-serif font-bold mb-10 text-[#c9a961] tracking-[0.2em] uppercase text-center md:text-left",
                    children: category.title
                }, void 0, false, {
                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx",
                    lineNumber: 57,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "grid md:grid-cols-2 gap-10",
                    children: category.items.map((item, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "bg-black p-8 rounded-none border border-[#c9a961]/30 flex flex-col justify-between hover:border-[#c9a961]/60 transition-colors duration-500",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "mb-8",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                            className: "text-2xl font-serif font-bold mb-4 text-[#c9a961] tracking-widest uppercase",
                                            children: item.name
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx",
                                            lineNumber: 69,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "w-12 h-px bg-[#c9a961]/40 mb-5"
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx",
                                            lineNumber: 72,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                            className: "text-[#f5f5f5]/80 font- italic leading-relaxed text-base md:text-lg font-light tracking-wide",
                                            children: item.desc
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx",
                                            lineNumber: 75,
                                            columnNumber: 17
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx",
                                    lineNumber: 67,
                                    columnNumber: 15
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                                    href: getWhatsAppLink(item.name),
                                    target: "_blank",
                                    rel: "noopener noreferrer",
                                    //class="w-16 h-16 bg-zinc-900 border border-[#c9a961]/20 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:border-[#c9a961]/50 transition-colors"
                                    className: "inline-flex items-center justify-center gap-3 bg-transparent border border-[#c9a961] text-[#c9a961] hover:bg-[#c9a961] hover:text-black font-bold py-4 px-6 rounded-none transition-all duration-700 ease-in-out active:bg-black active:text-[#c9a961] uppercase tracking-[0.3em] text-[10px]",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
                                            className: "w-4 h-4",
                                            fill: "currentColor",
                                            viewBox: "0 0 24 24",
                                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                                                d: "M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.588-5.946 0-6.556 5.332-11.891 11.891-11.891 3.181 0 6.167 1.24 8.413 3.488 2.248 2.248 3.488 5.236 3.488 8.413 0 6.557-5.332 11.892-11.891 11.892-1.997 0-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.438 9.886-9.886 0-5.448-4.438-9.886-9.886-9.886-5.448 0-9.885 4.438-9.885 9.886 0 2.221.634 4.317 1.834 6.085l-1.103 4.033 4.162-1.09z"
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx",
                                                lineNumber: 89,
                                                columnNumber: 19
                                            }, this)
                                        }, void 0, false, {
                                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx",
                                            lineNumber: 88,
                                            columnNumber: 17
                                        }, this),
                                        "Consultar Presupuesto"
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx",
                                    lineNumber: 81,
                                    columnNumber: 15
                                }, this)
                            ]
                        }, index, true, {
                            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx",
                            lineNumber: 63,
                            columnNumber: 13
                        }, this))
                }, void 0, false, {
                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx",
                    lineNumber: 61,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx",
            lineNumber: 50,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx",
        lineNumber: 49,
        columnNumber: 5
    }, this);
}
}),
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx [app-rsc] (ecmascript, Next.js Server Component)", ((__turbopack_context__) => {

__turbopack_context__.n(__turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/products/[categorie]/page.tsx [app-rsc] (ecmascript)"));
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__0b3fb99f._.js.map