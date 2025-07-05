// models/Journey.js
import mongoose from 'mongoose'

const touchpointSchema = new mongoose.Schema({
  stage: { type: String, required: true },   // z. B. Awareness, Consideration, etc.
  content: { type: String, required: true }, // Beschreibung z. B. "LinkedIn Ad"
  goal: String,                              // z. B. "Demo buchen"
  channel: String                            // z. B. "LinkedIn", "Newsletter"
})

const journeySchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  persona: { type: mongoose.Schema.Types.ObjectId, ref: 'Persona', required: true },
  name: { type: String, required: true },
  description: String,
  touchpoints: [touchpointSchema]
}, { timestamps: true })

const Journey = mongoose.model('Journey', journeySchema)
export default Journey
