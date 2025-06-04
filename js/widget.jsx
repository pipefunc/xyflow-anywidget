import * as React from "react";
import * as ReactDOM from "react-dom/client";
import { ReactFlow, Controls, Background } from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import "./widget.css";

function render({ model, el }) {
  let container = document.createElement("div");
  el.appendChild(container);

  const root = ReactDOM.createRoot(container);

  function update() {
    const nodes = model.get("nodes");
    const edges = model.get("edges");
    const rfProps = model.get("props") || {};
    const height = model.get("height") || "400px";
    const width = model.get("width") || "100%";

    root.render(
      React.createElement("div", {
        style: { position: "relative", height, width }
      },
        React.createElement(ReactFlow, {
          nodes: nodes,
          edges: edges,
          ...rfProps
        }, [
          React.createElement(Background, { key: "bg" }),
          React.createElement(Controls, { key: "controls" })
        ])
      )
    );
  }

  update();

  model.on("change:nodes", update);
  model.on("change:edges", update);
  model.on("change:props", update);
  model.on("change:height", update);
  model.on("change:width", update);

  return () => {
    model.off("change:nodes", update);
    model.off("change:edges", update);
    model.off("change:props", update);
    model.off("change:height", update);
    model.off("change:width", update);
    root.unmount();
  };
}

export default { render };
