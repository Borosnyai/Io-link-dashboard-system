// Simulated backend for the standalone demo.
// Replaces fetch() and WebSocket so the real, unchanged frontend runs without
// the Python service, the IO-Link master, MQTT or InfluxDB.
// All values are a pure function of time, so the history (last hour) and the
// live stream always match.

const API = 'http://localhost:8000'
const T0 = Date.now() / 1000          // page load = start of the scenario
const CYCLE = 240                     // seconds between simulated anomalies
const ANOMALY_START = 45              // first anomaly 45 s after page load

// ---------------------------------------------------------------- helpers
function noise(seed, t) {
  const x = Math.sin(Math.floor(t) * 12.9898 + seed * 78.233) * 43758.5453
  return (x - Math.floor(x)) * 2 - 1
}

// 0..1 progress inside the anomaly window of the current cycle
function anomaly(t, startOffset = 0, length = 36) {
  const phase = (((t - T0 - ANOMALY_START - startOffset) % CYCLE) + CYCLE) % CYCLE
  if (phase > length) return 0
  const x = phase / length
  return x < 0.5 ? x / 0.5 : 1 - (x - 0.5) / 0.5
}

const round = (v, d = 2) => Number(v.toFixed(d))

const toHex = (text) =>
  [...text].map((c) => c.charCodeAt(0).toString(16).padStart(2, '0')).join('').toUpperCase()

// ---------------------------------------------------------------- sensors
const SENSORS = {
  1: {
    port: 1,
    vendor_id: '310',
    device_id: '1560',
    vendor_name: 'ifm electronic gmbh',
    product_name: 'PN7570',
    article_number: 'PN7570',
    description: 'PN7570, Pressure sensor with display',
    device_family: 'PN pressure sensors',
    version: '1.1',
    release_date: '2022-01-21',
    min_cycle_time: '2.3 ms',
    pd_in: 'Bit length: 18 bit',
    profiles: [{ id: 1, name: 'Generic Profiled Sensor' }, { id: 32769, name: 'Multiple switching signal' }],
    serial: 'PN7570-000412',
    items: [
      { name: 'Pressure', description: 'Current pressure', unit: 'bar', bits: 16, type: 'UIntegerT',
        range: [0, 10], fn: (t) => 5 + 0.7 * Math.sin(t / 41) + 0.04 * noise(1, t) },
      { name: 'Switch status [OUT1].', description: 'Switching output OUT1', bits: 1, type: 'BooleanT',
        fn: (t) => (5 + 0.7 * Math.sin(t / 41) > 5.35 ? 1 : 0) },
      { name: 'Switch status [OUT2].', description: 'Switching output OUT2', bits: 1, type: 'BooleanT',
        fn: (t) => (5 + 0.7 * Math.sin(t / 41) < 4.65 ? 1 : 0) },
    ],
  },
  2: {
    port: 2,
    vendor_id: '310',
    device_id: '1782',
    vendor_name: 'ifm electronic gmbh',
    product_name: 'VVB001',
    article_number: 'VVB001',
    description: 'VVB001, Vibration sensor with temperature output',
    device_family: 'VVB vibration sensors',
    version: '1.1',
    release_date: '2024-05-16',
    min_cycle_time: '5.0 ms',
    pd_in: 'Bit length: 96 bit',
    profiles: [{ id: 1, name: 'Generic Profiled Sensor' }, { id: 32771, name: 'Device diagnosis' }],
    serial: 'VVB001-208871',
    items: [
      { name: 'Vibration v-RMS', description: 'Vibration velocity (RMS)', unit: 'mm/s', bits: 32, type: 'Float32T',
        fn: (t) => 1.8 + 0.25 * Math.sin(t / 23) + 0.08 * noise(2, t) + 6.5 * anomaly(t) * (0.85 + 0.15 * noise(3, t)) },
      { name: 'Temperature', description: 'Housing temperature', unit: '°C', bits: 32, type: 'Float32T',
        fn: (t) => 38 + 1.8 * Math.sin(t / 90) + 0.15 * noise(4, t) + 14 * anomaly(t, 4, 60) },
      { name: 'Acceleration a-Peak', description: 'Peak acceleration', unit: 'g', bits: 32, type: 'Float32T',
        fn: (t) => 0.9 + 0.12 * Math.sin(t / 19) + 0.05 * noise(5, t) + 2.4 * anomaly(t) },
    ],
  },
  3: {
    port: 3,
    vendor_id: '26',
    device_id: '263955',
    vendor_name: 'Balluff GmbH',
    product_name: 'BOD 24K-LI0x-S92',
    article_number: 'BOD0071',
    description: 'BOD 24K-LI0x-S92, Laser distance sensor',
    device_family: 'BOD optical distance sensors',
    version: '1.0.1',
    release_date: '2016-08-12',
    min_cycle_time: '1.0 ms',
    pd_in: 'Bit length: 17 bit',
    profiles: [{ id: 1, name: 'Generic Profiled Sensor' }],
    serial: 'BOD-31-775120',
    items: [
      { name: 'Distance', description: 'Measured distance', unit: 'mm', bits: 16, type: 'IntegerT',
        range: [50, 2000],
        specials: [{ value: 32760, name: 'OL' }, { value: -32760, name: 'UL' }, { value: 32764, name: 'NoData' }],
        fn: (t) => {
          const lost = anomaly(t, 20, 6) > 0.3
          return lost ? 32764 : Math.round(820 + 260 * Math.sin(t / 17) + 6 * noise(6, t))
        } },
      { name: 'Switching signal [OUT1]', description: 'Switching output', bits: 1, type: 'BooleanT',
        fn: (t) => (820 + 260 * Math.sin(t / 17) < 700 ? 1 : 0) },
    ],
  },
}

function datatypeOf(item) {
  const dt = { type: item.type, bit_length: item.bits }
  if (item.range) dt.value_ranges = [{ lower_value: item.range[0], upper_value: item.range[1] }]
  if (item.specials) dt.single_values = item.specials
  if (item.bits === 1) dt.single_values = [{ value: 0, name: 'Inactive' }, { value: 1, name: 'Active' }]
  return dt
}

function structureOf(sensor) {
  let offset = 0
  const items = [...sensor.items].reverse().map((item, i) => {
    const out = {
      subindex: i + 1,
      name: item.name,
      description: item.description,
      datatype: datatypeOf(item),
      bit_offset: offset,
      bit_length: item.bits,
      unit: item.unit ?? '',
    }
    offset += item.bits
    return out
  })
  return { count: 1, process_data: [{ name: 'Process Data In', bit_length: offset, items }] }
}

function valueOf(sensor, name, t) {
  const item = sensor.items.find((i) => i.name === name)
  const v = item.fn(t)
  return item.bits === 1 || Number.isInteger(v) ? v : round(v, item.unit === 'bar' ? 3 : 2)
}

// ------------------------------------------------------- IO-Link variables
const STD_VARIABLES = [
  { variable_id: 'V_DirectParameters_1', name: 'Direct Parameters Page 1', index: 0, access_rights: 'ro', items_count: 8 },
  { variable_id: 'V_SystemCommand', name: 'System Command', index: 2, access_rights: 'wo', items_count: 0 },
  { variable_id: 'V_DeviceAccessLocks', name: 'Device Access Locks', index: 12, access_rights: 'rw', items_count: 0 },
  { variable_id: 'V_VendorName', name: 'Vendor Name', index: 16, access_rights: 'ro', items_count: 0 },
  { variable_id: 'V_VendorText', name: 'Vendor Text', index: 17, access_rights: 'ro', items_count: 0 },
  { variable_id: 'V_ProductName', name: 'Product Name', index: 18, access_rights: 'ro', items_count: 0 },
  { variable_id: 'V_ProductID', name: 'Product ID', index: 19, access_rights: 'ro', items_count: 0 },
  { variable_id: 'V_ProductText', name: 'Product Text', index: 20, access_rights: 'ro', items_count: 0 },
  { variable_id: 'V_SerialNumber', name: 'Serial Number', index: 21, access_rights: 'ro', items_count: 0 },
  { variable_id: 'V_HardwareRevision', name: 'Hardware Revision', index: 22, access_rights: 'ro', items_count: 0 },
  { variable_id: 'V_FirmwareRevision', name: 'Firmware Revision', index: 23, access_rights: 'ro', items_count: 0 },
  { variable_id: 'V_ApplicationSpecificTag', name: 'Application Specific Tag', index: 24, access_rights: 'rw', items_count: 0 },
  { variable_id: 'V_DeviceStatus', name: 'Device Status', index: 36, access_rights: 'ro', items_count: 0 },
  { variable_id: 'V_ProcessDataInput', name: 'Process Data Input', index: 40, access_rights: 'ro', items_count: 0 },
]

const SPECIFIC_VARIABLES = {
  1: [
    { variable_id: 'V_SP1', name: 'Switchpoint SP1', index: 580, access_rights: 'rw', items_count: 0 },
    { variable_id: 'V_rP1', name: 'Reset point rP1', index: 581, access_rights: 'rw', items_count: 0 },
    { variable_id: 'V_OUT1_Mode', name: 'Output function OUT1', index: 582, access_rights: 'rw', items_count: 0 },
  ],
  2: [
    { variable_id: 'V_FrequencyRange', name: 'Frequency range', index: 600, access_rights: 'rw', items_count: 0 },
    { variable_id: 'V_AlarmLimitVrms', name: 'Alarm limit v-RMS', index: 601, access_rights: 'rw', items_count: 0 },
  ],
  3: [
    { variable_id: 'V_NearLimit', name: 'Near limit', index: 700, access_rights: 'rw', items_count: 0 },
    { variable_id: 'V_FarLimit', name: 'Far limit', index: 701, access_rights: 'rw', items_count: 0 },
  ],
}

const parameterStore = {}   // written values survive until the page is closed

function readParameter(sensor, index, subindex) {
  const key = `${sensor.port}:${index}:${subindex}`
  if (parameterStore[key]) return parameterStore[key]

  const text = {
    16: sensor.vendor_name,
    17: 'www.' + sensor.vendor_name.split(' ')[0].toLowerCase() + '.com',
    18: sensor.product_name,
    19: sensor.article_number,
    20: sensor.description.split(',')[1]?.trim() ?? sensor.description,
    21: sensor.serial,
    22: 'HW 01.02',
    23: 'FW 1.4.2',
    24: '***',
  }
  if (text[index]) return toHex(text[index])

  const numeric = { 12: '0000', 36: '00', 580: '0096', 581: '008C', 582: '01', 600: '03E8',
    601: '0064', 700: '0064', 701: '07D0', 40: '0000' }
  return numeric[index] ?? '00'
}

// ----------------------------------------------------------------- routing
const json = (data, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json' } })

function sensorFrom(params) {
  return SENSORS[Number(params.get('port'))] ?? SENSORS[1]
}

function route(method, url, body) {
  const { pathname, searchParams: q } = url

  if (pathname === '/scan') return json({ message: 'Scan successful.' })

  if (pathname === '/inventory') {
    return json(Object.values(SENSORS).map((s) => ({
      port: s.port, vendor_id: s.vendor_id, device_id: s.device_id, product_id: s.article_number,
      vendor_name: s.vendor_name, device_name: s.product_name, description: s.description,
    })))
  }

  if (pathname === '/master/ports') {
    return json(Object.values(SENSORS).map((s) => ({
      port: s.port, device_id: s.device_id, device_name: s.product_name, vendor: s.vendor_id,
    })))
  }

  if (pathname === '/iodd') {
    const s = sensorFrom(q)
    return json({
      vendor_id: Number(s.vendor_id), device_id: Number(s.device_id), vendor_name: s.vendor_name,
      product_name: s.product_name, article_number: s.article_number, description: s.description,
      device_family: s.device_family, io_link_revision: '1.1', version: s.version,
      release_date: s.release_date,
      transport: { bitrate: 'COM2 (38.4 kBaud)', min_cycle_time: s.min_cycle_time, sio_supported: 'Yes' },
      process_data_input: s.pd_in, process_data_output: 'None',
    })
  }

  if (pathname === '/features') {
    const s = sensorFrom(q)
    return json({ data_storage: 'Supported', block_parameter: 'Supported', profiles: s.profiles })
  }

  if (pathname === '/variables/full') {
    const s = sensorFrom(q)
    const variables = [...STD_VARIABLES, ...(SPECIFIC_VARIABLES[s.port] ?? [])]
    return json({ count: variables.length, variables })
  }

  if (pathname === '/process-data/profiles') {
    return json([{ id: 'v_PD', name: 'Process Data In', value: 1, active: true }])
  }

  if (pathname === '/process-data/' || pathname === '/process-data') {
    return json(structureOf(sensorFrom(q)))
  }

  if (pathname === '/process-data/history') {
    const s = sensorFrom(q)
    const name = q.get('variable')
    if (!s.items.some((i) => i.name === name)) return json({ port: s.port, variable: name, points: [] })
    const now = Date.now() / 1000
    const points = []
    for (let t = now - 3600; t <= now; t += 5) {
      points.push({ time: new Date(t * 1000).toISOString(), value: valueOf(s, name, t) })
    }
    return json({ port: s.port, variable: name, points })
  }

  const activate = pathname.match(/^\/process-data\/port\/(\d+)\/activate-streaming$/)
  if (activate) return json({ status: 'streaming activated' })

  const read = pathname.match(/^\/master\/port\/(\d+)\/read\/(\d+)\/(\d+)$/)
  if (read) {
    const s = SENSORS[Number(read[1])] ?? SENSORS[1]
    return json({ code: 200, data: { value: readParameter(s, Number(read[2]), Number(read[3])) } })
  }

  const write = pathname.match(/^\/master\/port\/(\d+)\/write$/)
  if (write && method === 'POST') {
    const payload = JSON.parse(body || '{}')
    parameterStore[`${write[1]}:${payload.index}:${payload.subindex ?? 0}`] = String(payload.value).toUpperCase()
    return json({ code: 200, data: {} })
  }

  return json({ detail: `Demo backend: no route for ${pathname}` }, 404)
}

// ------------------------------------------------------------------- fetch
const realFetch = window.fetch.bind(window)

window.fetch = async (input, init = {}) => {
  const target = typeof input === 'string' ? input : input.url
  if (!target.startsWith(API)) return realFetch(input, init)

  await new Promise((resolve) => setTimeout(resolve, 60 + Math.random() * 120))   // network feel
  return route((init.method ?? 'GET').toUpperCase(), new URL(target), init.body)
}

// --------------------------------------------------------------- WebSocket
const RealWebSocket = window.WebSocket
let masterCounter = 1000

class MockWebSocket {
  static CONNECTING = 0
  static OPEN = 1
  static CLOSING = 2
  static CLOSED = 3

  constructor(url) {
    this.url = url
    this.readyState = MockWebSocket.CONNECTING
    this.onopen = this.onmessage = this.onerror = this.onclose = null
    const port = Number(url.match(/port(\d+)\/processdata/)?.[1] ?? 1)
    this.sensor = SENSORS[port] ?? SENSORS[1]

    setTimeout(() => {
      if (this.readyState !== MockWebSocket.CONNECTING) return
      this.readyState = MockWebSocket.OPEN
      this.onopen?.({})
      this.timer = setInterval(() => this.push(), 1000)
      this.push()
    }, 250)
  }

  push() {
    if (this.readyState !== MockWebSocket.OPEN) return
    const now = Date.now()
    const t = now / 1000
    const values = this.sensor.items.map((item) => ({
      name: item.name,
      value: valueOf(this.sensor, item.name, t),
      unit: item.unit ?? '',
      datatype: null,
    }))
    this.onmessage?.({
      data: JSON.stringify({
        mqtt_received_at: new Date(now).toISOString(),
        master_counter: masterCounter++,
        values,
      }),
    })
  }

  send() {}

  close() {
    clearInterval(this.timer)
    this.readyState = MockWebSocket.CLOSED
    this.onclose?.({})
  }
}

window.WebSocket = function (url, protocols) {
  return String(url).startsWith('ws://localhost:8000')
    ? new MockWebSocket(url)
    : new RealWebSocket(url, protocols)
}
Object.assign(window.WebSocket, {
  CONNECTING: 0, OPEN: 1, CLOSING: 2, CLOSED: 3,
})
