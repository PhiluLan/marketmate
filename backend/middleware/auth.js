export const protect = (req, res, next) => {
  // Beispiel: req.user = decoded token
  req.user = { id: '686299aa372271a7fcb7b580' } // später ersetzen durch echten JWT-Check
  next()
}
