"use client";

interface PetrophysicsSettingsProps {
  settings: any;
  setSettings: (settings: any) => void;
  onAnalyze: () => void;
  analyzing: boolean;
}

export default function PetrophysicsSettings({
  settings,
  setSettings,
  onAnalyze,
  analyzing,
}: PetrophysicsSettingsProps) {

  function update(
    key: string,
    value: string
  ) {
    setSettings({
      ...settings,
      [key]: Number(value),
    });
  }

  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-5">

      <div className="mb-5">
        <h3 className="font-medium">
          Formation Evaluation Settings
        </h3>

        <p className="mt-1 text-xs text-gray-500">
          Configure assumptions and interpretation cutoffs.
        </p>
      </div>


      {/* Gamma Ray */}

      <div className="mb-6">

        <p className="mb-3 text-xs uppercase tracking-wider text-gray-500">
          Gamma Ray
        </p>

        <div className="grid grid-cols-2 gap-3">

          <SettingInput
            label="Clean GR"
            value={settings.gr_clean}
            onChange={(value) =>
              update("gr_clean", value)
            }
          />

          <SettingInput
            label="Shale GR"
            value={settings.gr_shale}
            onChange={(value) =>
              update("gr_shale", value)
            }
          />

        </div>

      </div>


      {/* Density */}

      <div className="mb-6">

        <p className="mb-3 text-xs uppercase tracking-wider text-gray-500">
          Density
        </p>

        <div className="grid grid-cols-2 gap-3">

          <SettingInput
            label="Matrix Density"
            value={settings.rho_matrix}
            step="0.01"
            onChange={(value) =>
              update("rho_matrix", value)
            }
          />

          <SettingInput
            label="Fluid Density"
            value={settings.rho_fluid}
            step="0.01"
            onChange={(value) =>
              update("rho_fluid", value)
            }
          />

        </div>

      </div>


      {/* Archie */}

      <div className="mb-6">

        <p className="mb-3 text-xs uppercase tracking-wider text-gray-500">
          Archie Parameters
        </p>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">

          <SettingInput
            label="Rw"
            value={settings.rw}
            step="0.001"
            onChange={(value) =>
              update("rw", value)
            }
          />

          <SettingInput
            label="a"
            value={settings.a}
            step="0.1"
            onChange={(value) =>
              update("a", value)
            }
          />

          <SettingInput
            label="m"
            value={settings.m}
            step="0.1"
            onChange={(value) =>
              update("m", value)
            }
          />

          <SettingInput
            label="n"
            value={settings.n}
            step="0.1"
            onChange={(value) =>
              update("n", value)
            }
          />

        </div>

      </div>


      {/* Pay */}

      <div className="mb-6">

        <p className="mb-3 text-xs uppercase tracking-wider text-gray-500">
          Pay Cutoffs
        </p>

        <div className="grid grid-cols-3 gap-3">

          <SettingInput
            label="Max Vsh"
            value={settings.vsh_cutoff}
            step="0.01"
            onChange={(value) =>
              update("vsh_cutoff", value)
            }
          />

          <SettingInput
            label="Min Phi"
            value={settings.porosity_cutoff}
            step="0.01"
            onChange={(value) =>
              update("porosity_cutoff", value)
            }
          />

          <SettingInput
            label="Max Sw"
            value={settings.sw_cutoff}
            step="0.01"
            onChange={(value) =>
              update("sw_cutoff", value)
            }
          />

        </div>

      </div>


         </div>
  );
}


function SettingInput({
  label,
  value,
  step = "0.01",
  onChange,
}: {
  label: string;
  value: number;
  step?: string;
  onChange: (value: string) => void;
}) {

  return (
    <label className="block">

      <span className="mb-1 block text-xs text-gray-500">
        {label}
      </span>

      <input
        type="number"
        step={step}
        value={value}
        onChange={(e) =>
          onChange(e.target.value)
        }
        className="
          w-full
          rounded-lg
          border
          border-white/10
          bg-black/30
          px-3
          py-2
          text-sm
          outline-none
          focus:border-white/30
        "
      />

    </label>
  );
}