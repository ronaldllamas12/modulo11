import api from './api'

export async function getMachines() {
  const { data } = await api.get('/machines')
  if (Array.isArray(data)) return data
  if (Array.isArray(data?.items)) return data.items
  if (Array.isArray(data?.data)) return data.data
  return []
}

export async function getMachineDashboard() {
  const { data } = await api.get('/machines/dashboard')
  if (Array.isArray(data)) return data
  if (Array.isArray(data?.items)) return data.items
  if (Array.isArray(data?.data)) return data.data
  return []
}

export async function updateMachineDashboardStatus(machineId, payload) {
  const { data } = await api.patch(`/machines/${machineId}/status`, payload)
  return data
}
