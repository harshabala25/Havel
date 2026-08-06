import { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

function App() {
  const [zipCode, setZipCode] = useState("")
  const [bedrooms, setBedrooms] = useState(1)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const rooms = [1, 2, 3, 4]

  const isValidZip = (zip) => /^\d{5}$/.test(zip)

  const handleOnClick = async () => {
    setError(null)

    if (!isValidZip(zipCode)) {
      setError("Please enter a valid 5-digit zip code.")
      return
    }

    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          zip_code: zipCode,
          bedrooms: bedrooms
        })
      })

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`)
      }

      const data = await response.json()
      setPrediction(data.predicted_rent)
    } catch (err) {
      setError("Couldn't reach the server. Please try again in a moment.")
      setPrediction(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <div>
        <h1>Havel</h1>
        <h2>Predicting Rent Prices in the DFW Area</h2>
      </div>

      <div>
        <h2>Enter a zipcode</h2>
        <input
          onChange={(e) => setZipCode(e.target.value)}
          type="text"
          placeholder="Zipcode (ex 75035)"
          value={zipCode}
        />
      </div>

      <div>
        <h2>Number of bedrooms</h2>
        <select
          value={bedrooms}
          onChange={(e) => setBedrooms(Number(e.target.value))}
        >
          {rooms.map((room) => (
            <option key={room} value={room}>
              {room}
            </option>
          ))}
        </select>
      </div>

      <div>
        <button onClick={handleOnClick} disabled={loading}>
          {loading ? "Predicting..." : "Submit"}
        </button>
      </div>

      {error && (
        <div>
          <p className="error">{error}</p>
        </div>
      )}

      <div>
        <h2>Rent Predicted</h2>
        <p className="rent">
          {prediction !== null ? `$${prediction.toFixed(2)}` : "—"}
        </p>
      </div>
    </>
  )
}
export default App