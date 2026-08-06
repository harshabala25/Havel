import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)
  const [zipCode, setZipCode] = useState("")
  const [bedrooms, setBedrooms] = useState(1)
  const [prediction, setPrediction] = useState(0)

  const rooms = [1,2,3,4]

  const handleOnClick = async () => {

    const response = await fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        zip_code: zipCode,
        bedrooms: bedrooms
      })
    })

    const data = await response.json()

    setPrediction(data.predicted_rent)

  }

  return (
    <>
      <div>
        <h1>Havel</h1>
        <h2>Predicting Rent Prices in the DFW Area</h2>
      </div>

      <div>
        <h2>Enter a zipcode</h2>
        <input onChange={(e) => setZipCode(e.target.value)} type="text" placeholder="Zipcode (ex 75035)" 
        value = {zipCode}
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
      <button onClick = {handleOnClick}> Submit </button> 
     </div>
    
   <div>
    <h2>Rent Predicted</h2>
    <p className = "rent">
     {prediction !== null ? `$${prediction.toFixed(2)}` : "—"}
    </p>
  </div>

    </>
  )
}
export default App