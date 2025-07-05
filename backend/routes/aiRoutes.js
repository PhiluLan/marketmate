// routes/aiRoutes.js
import express from 'express'
const router = express.Router()

router.post('/touchpoint-suggestion', async (req, res) => {
  const { phase, persona } = req.body

  // Platzhalter-Logik – später ersetzen durch OpenAI o.Ä.
  const ideas = {
    Awareness: `Blogartikel zu "${persona.name}" Herausforderungen`,
    Consideration: `Vergleichsseite über Lösungen für "${persona.name}"`,
    Decision: `Landingpage mit Fallstudie für "${persona.name}"`,
    Retention: `Exklusives Onboarding-Video für "${persona.name}"`,
    Advocacy: `Kunden-Referral-Programm für "${persona.name}"`
  }

  const idea = ideas[phase] || 'Touchpoint-Idee generieren'
  res.json({ suggestion: idea })
})

export default router
