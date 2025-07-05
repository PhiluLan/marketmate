// controllers/personaController.js
import Persona from '../models/Persona.js'

// Alle Personas für eingeloggten User
export const getPersonas = async (req, res) => {
  const personas = await Persona.find({ user: req.user.id })
  res.json(personas)
}

// Neue Persona anlegen
export const createPersona = async (req, res) => {
  const { name, description, goals, pains, touchpoints } = req.body
  const persona = new Persona({
    user: req.user.id,
    name,
    description,
    goals,
    pains,
    touchpoints
  })
  const created = await persona.save()
  res.status(201).json(created)
}

// Aktualisieren
export const updatePersona = async (req, res) => {
  const persona = await Persona.findById(req.params.id)
  if (persona.user.toString() !== req.user.id) {
    return res.status(403).json({ message: 'Nicht erlaubt' })
  }

  Object.assign(persona, req.body)
  const updated = await persona.save()
  res.json(updated)
}

// Löschen
export const deletePersona = async (req, res) => {
  try {
    const persona = await Persona.findById(req.params.id)

    if (!persona) {
      return res.status(404).json({ message: 'Persona nicht gefunden' })
    }

    // Fallback: wenn kein User gespeichert wurde
    if (!persona.user || persona.user.toString() !== req.user.id) {
      return res.status(403).json({ message: 'Nicht erlaubt' })
    }

    await persona.deleteOne()
    res.json({ message: 'Gelöscht' })
  } catch (error) {
    console.error('Fehler beim Löschen:', error)
    res.status(500).json({ message: 'Serverfehler beim Löschen' })
  }
}
