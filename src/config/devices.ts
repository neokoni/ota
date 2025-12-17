export interface VersionConfig {
  version: string;
  label: string;
  changelogJsonUrl?: string;
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

export const devices: DeviceConfig[] = [
  {
    codename: 'lemonades',
    name: 'OnePlus 9R',
    systems: [
      {
        name: 'AviumUI',
        description: '基于 Android',
        versions: [
          {
            version: 'avium-16',
            label: '最新发布',
            changelogJsonUrl: '/ota/lemonades.json'
          },
          {
            version: 'avium-15',
            label: '旧版本',
            changelogJsonUrl: '/ota/lemonades.json'
          }
        ]
      }
    ]
  },
  {
    codename: 'nabu',
    name: 'Xiaomi Pad 5',
    systems: [
      {
        name: 'AviumUI',
        description: '基于 Android',
        versions: [
          {
            version: 'avium-16',
            label: '最新发布',
            changelogJsonUrl: '/ota/nabu.json'
          }
        ]
      }
    ]
  }
];

export const getDevice = (codename: string): DeviceConfig | undefined => {
  return devices.find(d => d.codename === codename);
};

export const getSystem = (codename: string, systemName: string): SystemConfig | undefined => {
  const device = getDevice(codename);
  return device?.systems.find(s => s.name === systemName);
};
