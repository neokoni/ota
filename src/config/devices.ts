export interface Release {
  date: string;
  version?: string;
  changes: string[];
}

export interface VersionConfig {
  version: string;
  label: string;
  releases: Release[];
}

export interface SystemConfig {
  name: string;
  description: string;
  versions: VersionConfig[];
}

export interface DeviceConfig {
  codename: string;
  name: string;
  systems: SystemConfig[];
}

// Load all JSON files from src/ota directory
const deviceModules = import.meta.glob('@/ota/*.json', { eager: true });

export const devices: DeviceConfig[] = Object.values(deviceModules).map((mod: any) => mod.default || mod);

export const getDevice = (codename: string): DeviceConfig | undefined => {
  return devices.find(d => d.codename === codename);
};

export const getSystem = (codename: string, systemName: string): SystemConfig | undefined => {
  const device = getDevice(codename);
  return device?.systems.find(s => s.name === systemName);
};

