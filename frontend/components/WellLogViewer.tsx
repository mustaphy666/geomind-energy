"use client";

import dynamic from "next/dynamic";

const Plot = dynamic(
  () => import("react-plotly.js"),
  {
    ssr: false,
  }
);

interface WellLogViewerProps {
  data: any[];
}

export default function WellLogViewer({
  data,
}: WellLogViewerProps) {

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-[600px] text-gray-500">
        No well-log data available.
      </div>
    );
  }

  const depth = data.map(
    (row) => row.DEPTH
  );

  const gr = data.map(
    (row) => row.GR
  );

  const rt = data.map(
    (row) => row.RT
  );

  const rhob = data.map(
    (row) => row.RHOB
  );

  const nphi = data.map(
    (row) => row.NPHI
  );

  const pay = data.map(
    (row) => row.PAY ? 1 : 0
  );


  return (
    <div className="w-full overflow-hidden rounded-2xl border border-white/10 bg-black">

      <div className="border-b border-white/10 px-5 py-4">

        <h3 className="font-medium">
          Well Log Interpretation
        </h3>

        <p className="text-xs text-gray-500 mt-1">
          Interactive formation evaluation
        </p>

      </div>


      <div className="w-full overflow-x-auto">

        <Plot
          data={[
            {
              x: gr,
              y: depth,
              type: "scatter",
              mode: "lines",
              name: "GR",
              xaxis: "x",
              yaxis: "y",
            },

            {
              x: rt,
              y: depth,
              type: "scatter",
              mode: "lines",
              name: "RT",
              xaxis: "x2",
              yaxis: "y",
            },

            {
              x: rhob,
              y: depth,
              type: "scatter",
              mode: "lines",
              name: "RHOB",
              xaxis: "x3",
              yaxis: "y",
            },

            {
              x: nphi,
              y: depth,
              type: "scatter",
              mode: "lines",
              name: "NPHI",
              xaxis: "x3",
              yaxis: "y",
            },

            {
              x: pay,
              y: depth,
              type: "scatter",
              mode: "lines",
              fill: "tozerox",
              name: "PAY",
              xaxis: "x4",
              yaxis: "y",
            },
          ]}

          layout={{
            height: 850,

            paper_bgcolor: "black",
            plot_bgcolor: "black",

            font: {
              color: "white",
            },

            margin: {
              l: 70,
              r: 30,
              t: 40,
              b: 50,
            },

            xaxis: {
              domain: [0, 0.22],
              title: "GR",
            },

            xaxis2: {
              domain: [0.25, 0.47],
              title: "RT",
              type: "log",
            },

            xaxis3: {
              domain: [0.50, 0.72],
              title: "RHOB / NPHI",
            },

            xaxis4: {
              domain: [0.75, 1],
              title: "PAY",
              range: [0, 1],
            },

            yaxis: {
              title: "Depth",
              autorange: "reversed",
            },

            showlegend: true,

            legend: {
              orientation: "h",
            },

            hovermode: "y unified",
          }}

          config={{
            responsive: true,
            displaylogo: false,
          }}

          style={{
            width: "100%",
          }}
        />

      </div>

    </div>
  );
}