export const mockSensorData = [
  {
    id: 'V_SensorPrinciple',
    name: 'SensorPrinciple',
    index: 187,
    values: [
      {
        name: 'SensorPrinciple',
        subindex: 0,
        mappings: [
          { text: 'Diffuse', val: 0 },
          { text: 'Diffuse with background suppression', val: 1 },
          { text: 'Retro-reflective', val: 2 },
          { text: 'Through-beam emitter', val: 3 },
          { text: 'Through-beam receiver', val: 4 },
        ],
      },
    ],
  },
  {
    id: 'V_OutputType',
    name: 'Output Type',
    index: 180,
    values: [
      {
        name: 'Output Type OUT1',
        subindex: 1,
        mappings: [
          { text: 'PNP', val: 1 },
          { text: 'NPN', val: 2 },
          { text: 'Push-Pull', val: 3 },
        ],
      },
      {
        name: 'Output Type OUT2',
        subindex: 2,
        mappings: [
          { text: 'PNP', val: 1 },
          { text: 'NPN', val: 2 },
          { text: 'Push-Pull', val: 3 },
        ],
      },
    ],
  },
  {
    id: 'V_DeviceStatus',
    name: 'Device Status',
    index: 36,
    values: [
      {
        name: 'Device Status',
        subindex: 0,
        mappings: [
          { text: 'Device is OK', val: 0 },
          { text: 'Maintenance required', val: 1 },
          { text: 'Out of specification', val: 2 },
          { text: 'Functional check', val: 3 },
          { text: 'Failure', val: 4 },
        ],
      },
    ],
  },
  {
    id: 'V_TeachInChannel',
    name: 'Teach-In Channel',
    index: 58,
    values: [
      {
        name: 'Teach-In Channel',
        subindex: 0,
        mappings: [
          { text: 'Default BDC (BDC1)', val: 0 },
          { text: 'BDC1', val: 1 },
        ],
      },
    ],
  },
];
