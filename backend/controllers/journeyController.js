// controllers/journeyController.js
import Journey from '../models/Journey.js'

export const getJourneys = async (req, res) => {
  const journeys = await Journey.find({ user: req.user.id }).populate('persona')
  res.json(journeys)
}

export const createJourney = async (req, res) => {
  const { name, description, persona, touchpoints } = req.body
  const journey = new Journey({
    user: req.user.id,
    name,
    description,
    persona,
    touchpoints
  })
  const created = await journey.save()
  res.status(201).json(created)
}

export const updateJourney = async (req, res) => {
  const journey = await Journey.findById(req.params.id)
  if (!journey || journey.user.toString() !== req.user.id) {
    return res.status(403).json({ message: 'Nicht erlaubt' })
  }

  Object.assign(journey, req.body)
  const updated = await journey.save()
  res.json(updated)
}

export const deleteJourney = async (req, res) => {
  try {
    const journey = await Journey.findById(req.params.id)

    if (!journey) {
      return res.status(404).json({ message: 'Journey nicht gefunden' })
    }

    if (!journey.user || journey.user.toString() !== req.user.id) {
      return res.status(403).json({ message: 'Nicht erlaubt' })
    }

    await journey.deleteOne() // ✅ Richtiger Befehl
    res.json({ message: 'Journey gelöscht' })
  } catch (error) {
    console.error('Fehler beim Löschen der Journey:', error)
    res.status(500).json({ message: 'Serverfehler beim Löschen' })
  }
}
