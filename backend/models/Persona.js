// models/Persona.js
import mongoose from 'mongoose'

const touchpointSchema = new mongoose.Schema({
  stage: { type: String, required: true },       // Awareness, Consideration, etc.
  content: { type: String, required: true },     // Content-Idee oder Beschreibung
})

const personaSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
  },
  name: { type: String, required: true },
  description: String,
  goals: [String],
  pains: [String],
  touchpoints: [touchpointSchema], // Customer Journey Punkte
}, { timestamps: true })

const Persona = mongoose.model('Persona', personaSchema)
export default Persona
