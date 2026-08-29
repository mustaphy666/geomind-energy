"use client";

import {
  Layers3,
} from "lucide-react";


interface ReservoirIntervalTableProps {
  intervals: any[];
}


export default function ReservoirIntervalTable({
  intervals,
}: ReservoirIntervalTableProps) {

  if (!intervals.length) {
    return null;
  }


  return (
    <div className="
      mt-6
      overflow-hidden
      rounded-2xl
      border
      border-white/10
      bg-white/5
    ">

      <div className="
        border-b
        border-white/10
        px-5
        py-4
      ">

        <div className="
          flex
          items-center
          gap-3
        ">

          <Layers3 size={18} />

          <div>

            <p className="text-sm font-medium">
              Candidate Reservoir Intervals
            </p>

            <p className="
              text-xs
              text-gray-500
            ">
              Broader reservoir-quality
              intervals identified from
              log-derived properties
            </p>

          </div>

        </div>

      </div>


      <div className="overflow-x-auto">

        <table className="w-full text-sm">

          <thead>

            <tr className="
              border-b
              border-white/10
              text-xs
              text-gray-500
            ">

              <th className="
                px-5
                py-3
                text-left
              ">
                Zone
              </th>

              <th className="
                px-5
                py-3
                text-left
              ">
                Top
              </th>

              <th className="
                px-5
                py-3
                text-left
              ">
                Base
              </th>

              <th className="
                px-5
                py-3
                text-left
              ">
                Gross
              </th>

              <th className="
                px-5
                py-3
                text-left
              ">
                Avg Vsh
              </th>

              <th className="
                px-5
                py-3
                text-left
              ">
                Avg Phi
              </th>

              <th className="
                px-5
                py-3
                text-left
              ">
                Avg Sw
              </th>

            </tr>

          </thead>


          <tbody>

            {intervals.map(
              (interval, index) => (

                <tr
                  key={index}
                  className="
                    border-b
                    border-white/5
                    last:border-0
                    hover:bg-white/5
                  "
                >

                  <td className="px-5 py-4">
                    Zone {index + 1}
                  </td>

                  <td className="px-5 py-4">
                    {interval.top} ft
                  </td>

                  <td className="px-5 py-4">
                    {interval.base} ft
                  </td>

                  <td className="
                    px-5
                    py-4
                    font-medium
                  ">
                    {interval.gross_thickness} ft
                  </td>

                  <td className="px-5 py-4">
                    {(interval.average_vsh * 100).toFixed(1)}%
                  </td>

                  <td className="px-5 py-4">
                    {(interval.average_porosity * 100).toFixed(1)}%
                  </td>

                  <td className="px-5 py-4">
                    {(interval.average_sw * 100).toFixed(1)}%
                  </td>

                </tr>

              )
            )}

          </tbody>

        </table>

      </div>

    </div>
  );
}