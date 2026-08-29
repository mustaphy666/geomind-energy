"use client";

import {
  Layers3,
  ArrowUpDown,
} from "lucide-react";


interface PayIntervalTableProps {
  intervals: any[];
}


export default function PayIntervalTable({
  intervals,
}: PayIntervalTableProps) {

  if (!intervals || intervals.length === 0) {

    return (
      <div className="
        mt-6
        rounded-2xl
        border
        border-white/10
        bg-white/5
        p-6
      ">

        <div className="flex items-center gap-3">

          <Layers3 size={18} />

          <div>

            <p className="text-sm font-medium">
              Potential Pay Intervals
            </p>

            <p className="text-xs text-gray-500">
              No intervals meet the current
              interpretation criteria.
            </p>

          </div>

        </div>

      </div>
    );
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

        <div className="flex items-center gap-3">

          <Layers3 size={18} />

          <div>

            <p className="text-sm font-medium">
              Potential Pay Intervals
            </p>

            <p className="text-xs text-gray-500">
              {intervals.length} candidate
              interval
              {intervals.length !== 1
                ? "s"
                : ""}
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

              <th className="px-5 py-3 text-left">
                Rank
              </th>

              <th className="px-5 py-3 text-left">
                Top
              </th>

              <th className="px-5 py-3 text-left">
                Base
              </th>

              <th className="px-5 py-3 text-left">
                Thickness
              </th>

              <th className="px-5 py-3 text-left">
                Vsh
              </th>

              <th className="px-5 py-3 text-left">
                Porosity
              </th>

              <th className="px-5 py-3 text-left">
                Sw
              </th>

            </tr>

          </thead>


          <tbody>

            {(intervals || []).map(
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
                    #{interval.rank}
                  </td>

                  <td className="px-5 py-4">
                    {interval.top.toFixed(1)} m
                  </td>

                  <td className="px-5 py-4">
                    {interval.base.toFixed(1)} m
                  </td>

                  <td className="
                    px-5
                    py-4
                    font-medium
                  ">
                    {interval?.thickness != null ? interval.thickness.toFixed(1) : "0.0"} m
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