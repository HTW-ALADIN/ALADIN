export interface GraphStyle {
	type?: "graph" | "digraph";
	bgcolor?: keyof typeof GraphColors;
	splines?: keyof typeof SplineTypes;
	rankdir?: "LR" | "RL" | "TB" | "BT";
}

export interface NodeStyle {
	shape?: keyof typeof NodeShapes;
	style?: string;
}

export interface EdgeStyle {
	dir?: "forward" | "back";
	style?: Styles;
}

export enum SplineTypes {
	true = "true",
	false = "false",
	polyline = "polyline",
	ortho = "ortho",
	curved = "curved",
}

export enum GraphColors {
	transparent = "transparent",
}

export enum Styles {
	dashed = "dashed",
	dotted = "dotted",
	solid = "solid",
	invis = "inivis",
	bold = "bold",
	tapered = "tapered",
	filled = "filled",
	striped = "striped",
	wedged = "wedged",
	diagonals = "diagonals",
	rounded = "rounded",
	radial = "radial",
}

export enum NodeShapes {
	box = "box",
	polygon = "polygon",
	ellipse = "ellipse",
	oval = "oval",
	circle = "circle",
	point = "point",
	egg = "egg",
	triangle = "triangle",
	plaintext = "plaintext",
	plain = "plain",
	diamond = "diamond",
	trapezium = "trapezium",
	parallelogram = "parallelogram",
	house = "house",
	pentagon = "pentagon",
	hexagon = "hexagon",
	septagon = "septagon",
	octagon = "octagon",
	doublecircle = "doublecircle",
	doubleoctagon = "doubleoctagon",
	tripleoctagon = "tripleoctagon",
	invtriangle = "invtriangle",
	invtrapezium = "invtrapezium",
	invhouse = "invhouse",
	Mdiamond = "Mdiamond",
	Msquare = "Msquare",
	Mcircle = "Mcircle",
	rect = "rect",
	rectangle = "rectangle",
	square = "square",
	star = "star",
	none = "none",
	underline = "underline",
	cylinder = "cylinder",
	note = "note",
	tab = "tab",
	folder = "folder",
	box3d = "box3d",
	component = "component",
	promoter = "promoter",
	cds = "cds",
	terminator = "terminator",
	utr = "utr",
	primersite = "primersite",
	restrictionsite = "restrictionsite",
	fivepoverhang = "fivepoverhang",
	threepoverhang = "threepoverhang",
	noverhang = "noverhang",
	assembly = "assembly",
	signature = "signature",
	insulator = "insulator",
	ribosite = "ribosite",
	rnastab = "rnastab",
	proteasesite = "proteasesite",
	proteinstab = "proteinstab",
	rpromoter = "rpromoter",
	rarrow = "rarrow",
	larrow = "larrow",
	lpromoter = "lpromoter",
	record = "record",
}

export enum EdgeShapes {
	box = "box",
	lbox = "lbox",
	rbox = "rbox",
	obox = "obox",
	olbox = "olbox",
	orbox = "orbox",
	crow = "crow",
	lcrow = "lcrow",
	rcrow = "rcrow",
	diamond = "diamond",
	ldiamond = "ldiamond",
	rdiamond = "rdiamond",
	odiamond = "odiamond",
	oldiamond = "oldiamond",
	ordiamond = "ordiamond",
	dot = "dot",
	odot = "odot",
	inv = "inv",
	linv = "linv",
	rinv = "rinv",
	oinv = "oinv",
	olinv = "olinv",
	orinv = "orinv",
	none = "none",
	normal = "normal",
	lnormal = "lnormal",
	rnormal = "rnormal",
	onormal = "onormal",
	olnormal = "olnormal",
	ornormal = "ornormal",
	tee = "tee",
	ltee = "ltee",
	rtee = "rtee",
	vee = "vee",
	lvee = "lvee",
	rvee = "rvee",
	curve = "curve",
	lcurve = "lcurve",
	rcurve = "rcurve",
	icurve = "icurve",
	licurve = "licurve",
	ricurve = "ricurve",
}
