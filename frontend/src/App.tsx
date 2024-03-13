import { useState, useRef } from "react";
import { Stage, Layer, Line } from "react-konva";
import type Konva from "konva";
import type { KonvaEventObject } from "konva/lib/Node";

type CustomLine = {
	points: number[];
};

function App() {
	const [lines, setLines] = useState<Array<CustomLine>>([]);
	const isDrawing = useRef(false);
	const stageRef = useRef<Konva.Stage>(null);

	const handleExport = async () => {
		if (!stageRef.current) return;
		console.log(stageRef.current);
		const blob = await stageRef.current.toBlob();

		// TODO: Core logic involving the backend
		// Use fetch

		// Reset
		setLines([]);
	};

	const handleMouseDown = (e: KonvaEventObject<MouseEvent>) => {
		isDrawing.current = true;
		const pos = e.target.getStage()?.getPointerPosition();
		if (!pos) return;
		setLines((lines) => [...lines, { points: [pos.x, pos.y] }]);
	};

	const handleMouseMove = (e: KonvaEventObject<MouseEvent>) => {
		// no drawing - skipping
		if (!isDrawing.current) return;
		const point = e.target.getStage()?.getPointerPosition();
		if (!point) return;
		const lastLine = lines[lines.length - 1];
		// add point
		lastLine.points = lastLine.points.concat([point.x, point.y]);

		// replace last
		lines.splice(lines.length - 1, 1, lastLine);
		setLines(lines.concat());
	};

	const handleMouseUp = () => {
		isDrawing.current = false;
	};

	return (
		<div className="mt-5 ml-5">
			<div>
				<button
					type="button"
					className="border-grey-500 border-2 rounded-full p-2 bg-grey-200"
					onClick={() => {
						setLines([]);
					}}
				>
					Erase
				</button>
				<button
					type="button"
					onClick={handleExport}
					className="border-yellow-500 border-2 rounded-full p-2 bg-yellow-200 ml-2"
				>
					Export to IMG
				</button>
			</div>
			<div className="w-[310px] h-[310px] border-[5px] border-black mt-4">
				<Stage
					width={300}
					height={300}
					onMouseDown={handleMouseDown}
					onMouseMove={handleMouseMove}
					onMouseUp={handleMouseUp}
					ref={stageRef}
				>
					<Layer>
						{lines.map((line, i) => (
							<Line
								key={i}
								points={line.points}
								stroke="#df4b26"
								strokeWidth={5}
								tension={0.5}
								lineCap="round"
								lineJoin="round"
								globalCompositeOperation={
									// line.tool === "eraser" ? "destination-out" : "source-over"
									"source-over"
								}
							/>
						))}
					</Layer>
				</Stage>
			</div>
		</div>
	);
}

export default App;
