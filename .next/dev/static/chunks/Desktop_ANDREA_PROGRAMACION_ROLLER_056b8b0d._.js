(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>CuttingCalculator
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$calculator$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Calculator$3e$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/icons/calculator.js [app-client] (ecmascript) <export default as Calculator>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$scissors$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Scissors$3e$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/icons/scissors.js [app-client] (ecmascript) <export default as Scissors>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$triangle$2d$alert$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__AlertTriangle$3e$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/icons/triangle-alert.js [app-client] (ecmascript) <export default as AlertTriangle>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$check$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Check$3e$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/icons/check.js [app-client] (ecmascript) <export default as Check>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$lib$2f$utils$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/lib/utils.ts [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
;
function CuttingCalculator({ rolls, onDiscountStock }) {
    _s();
    const [windowWidth, setWindowWidth] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [windowHeight, setWindowHeight] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [selectedRollId, setSelectedRollId] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])("");
    const [confirmed, setConfirmed] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const calculation = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useMemo"])({
        "CuttingCalculator.useMemo[calculation]": ()=>{
            const w = parseFloat(windowWidth);
            const h = parseFloat(windowHeight);
            if (isNaN(w) || isNaN(h) || w <= 0 || h <= 0) return null;
            const adjustedWidth = w + 10;
            const adjustedHeight = h + 30;
            const linearMeters = adjustedHeight / 100;
            return {
                windowWidthCm: w,
                windowHeightCm: h,
                adjustedWidthCm: adjustedWidth,
                adjustedHeightCm: adjustedHeight,
                linearMeters: Math.round(linearMeters * 100) / 100,
                selectedRollId: selectedRollId || null
            };
        }
    }["CuttingCalculator.useMemo[calculation]"], [
        windowWidth,
        windowHeight,
        selectedRollId
    ]);
    const selectedRoll = rolls.find((r)=>r.id === selectedRollId);
    // --- FUNCIÓN DE NORMALIZACIÓN DE ANCHO (Metros o CM) ---
    const getRollWidthInCm = (roll)=>{
        if (!roll) return 0;
        const w = Number(roll.widthCm);
        // Si el valor es pequeño (ej: 2.1), son metros. Si es grande (ej: 210), son cm.
        return w < 10 ? w * 100 : w;
    };
    const canConfirm = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useMemo"])({
        "CuttingCalculator.useMemo[canConfirm]": ()=>{
            if (!calculation || !selectedRoll) return false;
            // 1. Validar Largo (Stock disponible)
            const tieneStockLargo = calculation.linearMeters <= Number(selectedRoll.metersLeft);
            // 2. Validar Ancho (Físico de la tela)
            const anchoRolloCm = getRollWidthInCm(selectedRoll);
            const cabeAncho = calculation.adjustedWidthCm <= anchoRolloCm;
            return tieneStockLargo && cabeAncho;
        }
    }["CuttingCalculator.useMemo[canConfirm]"], [
        calculation,
        selectedRoll
    ]);
    const estimatedPrice = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useMemo"])({
        "CuttingCalculator.useMemo[estimatedPrice]": ()=>{
            if (!calculation || !selectedRoll) return 0;
            return Math.round(calculation.linearMeters * selectedRoll.pricePerMeter);
        }
    }["CuttingCalculator.useMemo[estimatedPrice]"], [
        calculation,
        selectedRoll
    ]);
    function handleConfirm() {
        if (!canConfirm || !calculation || !selectedRollId) return;
        onDiscountStock(selectedRollId, calculation.linearMeters);
        setConfirmed(true);
        setTimeout(()=>{
            setConfirmed(false);
            handleReset();
        }, 3000);
    }
    function handleReset() {
        setWindowWidth("");
        setWindowHeight("");
        setSelectedRollId("");
        setConfirmed(false);
    }
    const availableRolls = rolls.filter((r)=>Number(r.metersLeft) > 0);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex flex-col gap-6",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                        className: "font-serif text-2xl text-[#f5f0e8]",
                        children: "Calculadora de Corte"
                    }, void 0, false, {
                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                        lineNumber: 88,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-sm text-[#6b6560] mt-1",
                        children: "Gestión de stock para AMARIGOM DECO"
                    }, void 0, false, {
                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                        lineNumber: 89,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                lineNumber: 87,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "grid grid-cols-1 lg:grid-cols-2 gap-6",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "bg-[#111111] border border-[#2a2520] rounded-lg p-6 flex flex-col gap-5",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex items-center gap-2 text-[#c9a961] mb-1",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$calculator$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Calculator$3e$__["Calculator"], {
                                        size: 18
                                    }, void 0, false, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                        lineNumber: 95,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                        className: "font-serif text-lg",
                                        children: "Medidas de la ventana"
                                    }, void 0, false, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                        lineNumber: 96,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                lineNumber: 94,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "grid grid-cols-2 gap-4",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                className: "block text-xs text-[#6b6560] uppercase mb-2",
                                                children: "Ancho (cm)"
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                lineNumber: 101,
                                                columnNumber: 15
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                type: "number",
                                                value: windowWidth,
                                                onChange: (e)=>{
                                                    setWindowWidth(e.target.value);
                                                    setConfirmed(false);
                                                },
                                                placeholder: "150",
                                                className: "w-full bg-[#0a0a0a] border border-[#2a2520] rounded-lg px-4 py-3 text-[#f5f0e8] focus:border-[#c9a961] outline-none"
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                lineNumber: 102,
                                                columnNumber: 15
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                        lineNumber: 100,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                className: "block text-xs text-[#6b6560] uppercase mb-2",
                                                children: "Alto (cm)"
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                lineNumber: 111,
                                                columnNumber: 15
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                                type: "number",
                                                value: windowHeight,
                                                onChange: (e)=>{
                                                    setWindowHeight(e.target.value);
                                                    setConfirmed(false);
                                                },
                                                placeholder: "200",
                                                className: "w-full bg-[#0a0a0a] border border-[#2a2520] rounded-lg px-4 py-3 text-[#f5f0e8] focus:border-[#c9a961] outline-none"
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                lineNumber: 112,
                                                columnNumber: 15
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                        lineNumber: 110,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                lineNumber: 99,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                        className: "block text-xs text-[#6b6560] uppercase mb-2",
                                        children: "Seleccionar rollo de tela"
                                    }, void 0, false, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                        lineNumber: 123,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                        value: selectedRollId,
                                        onChange: (e)=>{
                                            setSelectedRollId(e.target.value);
                                            setConfirmed(false);
                                        },
                                        className: "w-full bg-[#0a0a0a] border border-[#2a2520] rounded-lg px-4 py-3 text-[#f5f0e8] focus:border-[#c9a961] transition-colors outline-none",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                value: "",
                                                children: "-- Seleccionar rollo --"
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                lineNumber: 129,
                                                columnNumber: 15
                                            }, this),
                                            availableRolls.map((roll)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                    value: roll.id,
                                                    children: [
                                                        roll.name,
                                                        " (",
                                                        roll.metersLeft,
                                                        "m disp. - ",
                                                        getRollWidthInCm(roll),
                                                        "cm ancho)"
                                                    ]
                                                }, roll.id, true, {
                                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                    lineNumber: 131,
                                                    columnNumber: 17
                                                }, this))
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                        lineNumber: 124,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                lineNumber: 122,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex gap-3 mt-2",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: handleConfirm,
                                        disabled: !canConfirm || confirmed,
                                        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$lib$2f$utils$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["cn"])("flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg text-sm font-medium transition-all", confirmed ? "bg-[#7a9b76] text-[#0a0a0a]" : canConfirm ? "bg-[#c9a961] text-[#0a0a0a] hover:bg-[#d4b574]" : "bg-[#1a1a1a] text-[#3a3530] cursor-not-allowed"),
                                        children: confirmed ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$check$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Check$3e$__["Check"], {
                                                    size: 16
                                                }, void 0, false, {
                                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                    lineNumber: 147,
                                                    columnNumber: 30
                                                }, this),
                                                " ¡Stock actualizado!"
                                            ]
                                        }, void 0, true) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$scissors$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Scissors$3e$__["Scissors"], {
                                                    size: 16
                                                }, void 0, false, {
                                                    fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                    lineNumber: 147,
                                                    columnNumber: 77
                                                }, this),
                                                " Confirmar y descontar stock"
                                            ]
                                        }, void 0, true)
                                    }, void 0, false, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                        lineNumber: 139,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: handleReset,
                                        className: "px-4 py-3 rounded-lg text-sm border border-[#2a2520] text-[#6b6560] hover:text-white",
                                        children: "Limpiar"
                                    }, void 0, false, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                        lineNumber: 149,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                lineNumber: 138,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                        lineNumber: 93,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex flex-col gap-4",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "bg-[#111111] border border-[#2a2520] rounded-lg p-6",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                        className: "font-serif text-lg text-[#c9a961] mb-4",
                                        children: "Resultado del cálculo"
                                    }, void 0, false, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                        lineNumber: 157,
                                        columnNumber: 13
                                    }, this),
                                    calculation ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "flex flex-col gap-4",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "grid grid-cols-2 gap-4",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "bg-[#0a0a0a] rounded-lg p-4",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                className: "text-[10px] text-[#6b6560] uppercase",
                                                                children: "Ancho + Margen (+10)"
                                                            }, void 0, false, {
                                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                                lineNumber: 163,
                                                                columnNumber: 21
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                className: "text-lg text-[#c9a961] font-serif",
                                                                children: [
                                                                    calculation.adjustedWidthCm,
                                                                    " cm"
                                                                ]
                                                            }, void 0, true, {
                                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                                lineNumber: 164,
                                                                columnNumber: 21
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                        lineNumber: 162,
                                                        columnNumber: 19
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                        className: "bg-[#0a0a0a] rounded-lg p-4",
                                                        children: [
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                className: "text-[10px] text-[#6b6560] uppercase",
                                                                children: "Alto + Margen (+30)"
                                                            }, void 0, false, {
                                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                                lineNumber: 167,
                                                                columnNumber: 21
                                                            }, this),
                                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                                className: "text-lg text-[#c9a961] font-serif",
                                                                children: [
                                                                    calculation.adjustedHeightCm,
                                                                    " cm"
                                                                ]
                                                            }, void 0, true, {
                                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                                lineNumber: 168,
                                                                columnNumber: 21
                                                            }, this)
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                        lineNumber: 166,
                                                        columnNumber: 19
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                lineNumber: 161,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "bg-[#c9a961]/5 border border-[#c9a961]/20 rounded-lg p-5 text-center",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                        className: "text-xs text-[#c9a961] uppercase mb-1",
                                                        children: "Metros lineales necesarios"
                                                    }, void 0, false, {
                                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                        lineNumber: 173,
                                                        columnNumber: 19
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                        className: "text-4xl font-serif text-[#c9a961]",
                                                        children: [
                                                            calculation.linearMeters,
                                                            " m"
                                                        ]
                                                    }, void 0, true, {
                                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                        lineNumber: 174,
                                                        columnNumber: 19
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                lineNumber: 172,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                        lineNumber: 160,
                                        columnNumber: 15
                                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "flex flex-col items-center py-8 text-[#2a2520]",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$calculator$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__Calculator$3e$__["Calculator"], {
                                                size: 40,
                                                className: "mb-3"
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                lineNumber: 179,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                className: "text-sm text-[#6b6560]",
                                                children: "Ingresá medidas para ver el cálculo"
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                lineNumber: 180,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                        lineNumber: 178,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                lineNumber: 156,
                                columnNumber: 11
                            }, this),
                            calculation && selectedRoll && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex flex-col gap-2",
                                children: [
                                    calculation.adjustedWidthCm > getRollWidthInCm(selectedRoll) && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "flex items-center gap-2 bg-[#c97676]/10 border border-[#c97676]/20 rounded-lg px-4 py-3 text-[#c97676]",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$triangle$2d$alert$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__AlertTriangle$3e$__["AlertTriangle"], {
                                                size: 16,
                                                className: "flex-shrink-0"
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                lineNumber: 190,
                                                columnNumber: 19
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                className: "text-xs",
                                                children: [
                                                    "El ancho ajustado (",
                                                    calculation.adjustedWidthCm,
                                                    "cm) supera el ancho del rollo (",
                                                    getRollWidthInCm(selectedRoll),
                                                    "cm). La cortina no entra."
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                lineNumber: 191,
                                                columnNumber: 19
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                        lineNumber: 189,
                                        columnNumber: 17
                                    }, this),
                                    calculation.linearMeters > Number(selectedRoll.metersLeft) && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "flex items-center gap-2 bg-[#c97676]/10 border border-[#c97676]/20 rounded-lg px-4 py-3 text-[#c97676]",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$triangle$2d$alert$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__default__as__AlertTriangle$3e$__["AlertTriangle"], {
                                                size: 16,
                                                className: "flex-shrink-0"
                                            }, void 0, false, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                lineNumber: 198,
                                                columnNumber: 19
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                className: "text-xs",
                                                children: [
                                                    "Stock insuficiente en metros lineales (",
                                                    selectedRoll.metersLeft,
                                                    "m disponibles)"
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                                lineNumber: 199,
                                                columnNumber: 19
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                        lineNumber: 197,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                                lineNumber: 187,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                        lineNumber: 155,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
                lineNumber: 92,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx",
        lineNumber: 86,
        columnNumber: 5
    }, this);
}
_s(CuttingCalculator, "YlGd7JekPTs0vtApH9yeUeYbW+Y=");
_c = CuttingCalculator;
var _c;
__turbopack_context__.k.register(_c, "CuttingCalculator");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/(admin)/gestion/calculadora/page.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>CalculadoraPage
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$components$2f$dashboard$2f$CuttingCalculator$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/components/dashboard/CuttingCalculator.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
function CalculadoraPage() {
    _s();
    const [rolls, setRolls] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    // Función para cargar o refrescar los rollos
    const loadInventory = async ()=>{
        try {
            const res = await fetch("/api/inventory");
            const data = await res.json();
            setRolls(data);
        } catch (error) {
            console.error("Error cargando inventario:", error);
        }
    };
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "CalculadoraPage.useEffect": ()=>{
            loadInventory();
        }
    }["CalculadoraPage.useEffect"], []);
    // Esta es la función que llama el componente cuando confirmás un corte
    const handleDiscountStock = async (rollId, meters)=>{
        try {
            const response = await fetch("/api/inventory", {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    id: rollId,
                    usedMeters: meters
                })
            });
            if (response.ok) {
                const updatedInventory = await response.json();
                setRolls(updatedInventory); // Actualiza la lista localmente
                alert("¡Corte registrado! El stock de AMARIGOM DECO ha sido actualizado.");
            } else {
                alert("No se pudo actualizar el stock. Verificá la conexión.");
            }
        } catch (error) {
            console.error("Error en la operación:", error);
            alert("Error crítico al procesar el descuento.");
        }
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "max-w-6xl mx-auto p-6",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-8",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                        className: "font-serif text-3xl text-[#f5f0e8]",
                        children: "Calculadora de Cortes"
                    }, void 0, false, {
                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/(admin)/gestion/calculadora/page.tsx",
                        lineNumber: 53,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "text-[#6b6560]",
                        children: "Calculá medidas y descontá stock automáticamente"
                    }, void 0, false, {
                        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/(admin)/gestion/calculadora/page.tsx",
                        lineNumber: 54,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/(admin)/gestion/calculadora/page.tsx",
                lineNumber: 52,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$components$2f$dashboard$2f$CuttingCalculator$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                rolls: rolls,
                onDiscountStock: handleDiscountStock
            }, void 0, false, {
                fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/(admin)/gestion/calculadora/page.tsx",
                lineNumber: 57,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/app/(admin)/gestion/calculadora/page.tsx",
        lineNumber: 51,
        columnNumber: 5
    }, this);
}
_s(CalculadoraPage, "4584esAGb88NkQecfq/u3L05G/o=");
_c = CalculadoraPage;
var _c;
__turbopack_context__.k.register(_c, "CalculadoraPage");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/icons/scissors.js [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.454.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "default",
    ()=>Scissors
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-client] (ecmascript)");
;
const Scissors = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"])("Scissors", [
    [
        "circle",
        {
            cx: "6",
            cy: "6",
            r: "3",
            key: "1lh9wr"
        }
    ],
    [
        "path",
        {
            d: "M8.12 8.12 12 12",
            key: "1alkpv"
        }
    ],
    [
        "path",
        {
            d: "M20 4 8.12 15.88",
            key: "xgtan2"
        }
    ],
    [
        "circle",
        {
            cx: "6",
            cy: "18",
            r: "3",
            key: "fqmcym"
        }
    ],
    [
        "path",
        {
            d: "M14.8 14.8 20 20",
            key: "ptml3r"
        }
    ]
]);
;
 //# sourceMappingURL=scissors.js.map
}),
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/icons/scissors.js [app-client] (ecmascript) <export default as Scissors>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Scissors",
    ()=>__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$scissors$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"]
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$scissors$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/icons/scissors.js [app-client] (ecmascript)");
}),
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/icons/triangle-alert.js [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.454.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "default",
    ()=>TriangleAlert
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-client] (ecmascript)");
;
const TriangleAlert = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"])("TriangleAlert", [
    [
        "path",
        {
            d: "m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3",
            key: "wmoenq"
        }
    ],
    [
        "path",
        {
            d: "M12 9v4",
            key: "juzpu7"
        }
    ],
    [
        "path",
        {
            d: "M12 17h.01",
            key: "p32p05"
        }
    ]
]);
;
 //# sourceMappingURL=triangle-alert.js.map
}),
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/icons/triangle-alert.js [app-client] (ecmascript) <export default as AlertTriangle>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "AlertTriangle",
    ()=>__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$triangle$2d$alert$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"]
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$triangle$2d$alert$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/icons/triangle-alert.js [app-client] (ecmascript)");
}),
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/icons/check.js [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.454.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "default",
    ()=>Check
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-client] (ecmascript)");
;
const Check = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"])("Check", [
    [
        "path",
        {
            d: "M20 6 9 17l-5-5",
            key: "1gmf2c"
        }
    ]
]);
;
 //# sourceMappingURL=check.js.map
}),
"[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/icons/check.js [app-client] (ecmascript) <export default as Check>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Check",
    ()=>__TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$check$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"]
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Desktop$2f$ANDREA$2f$PROGRAMACION$2f$ROLLER$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$check$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Desktop/ANDREA/PROGRAMACION/ROLLER/node_modules/lucide-react/dist/esm/icons/check.js [app-client] (ecmascript)");
}),
]);

//# sourceMappingURL=Desktop_ANDREA_PROGRAMACION_ROLLER_056b8b0d._.js.map