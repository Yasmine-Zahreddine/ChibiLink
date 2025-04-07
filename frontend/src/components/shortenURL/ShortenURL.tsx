import { useState } from 'react'
import Button from '../button/Button'
import DisplayURL from '../displayURL/DisplayURL'
import './shortenURL.css'

function ShortenURL() {
  const [inputUrl, setInputUrl] = useState('')
  const [shortenedUrl, setShortenedUrl] = useState('')
  const [expirationDate, setExpirationDate] = useState('')
  const [oneTimeClick, setOneTimeClick] = useState(false)
  const [urlLength, setUrlLength] = useState(6)
  const [error, setError] = useState('')

  const handleShorten = async () => {
    // Reset error state
    setError('')
    if(!inputUrl){
      setError('Please enter a URL')
      return
    }
    // Validation
    if (!expirationDate) {
      setError('Please set an expiration date')
      return
    }

    if (!urlLength || urlLength < 4 || urlLength > 10) {
      setError('URL length must be between 4 and 10 characters')
      return
    }

    try {
      const response = await fetch(`${import.meta.env.VITE_BASE_URL}/shorten`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          url: inputUrl.trim(),
          expiration_date: expirationDate,
          one_time_click: oneTimeClick,
          length: urlLength
        })
      });

      if (!response.ok) {
        if (response.status === 402) {
          setError('URL blocked due to suspicious content. Please try another URL.');
          return;
        }
        if (response.status === 429) {
          setError('Too many requests. Please try again later.');
          return;
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if(data.error){
        setError(data.error)}
        
      setShortenedUrl(data.new_url);
    } catch (error) {
      console.error('Error shortening URL:', error);
      setError('Failed to shorten URL. Please try again.')
    }
  }

  return (
    <div>
      <div className='shortenURL'>
        <input 
          type="text" 
          placeholder="Enter your URL here" 
          className='shortenURL_input'
          value={inputUrl}
          onChange={(e) => setInputUrl(e.target.value)}
          required
        />
        <div className='option-group-container'>
          <div className='option-group'>
            <label htmlFor="expiration">Expiration Date:</label>
            <input
              type="datetime-local"
              id="expiration"
              value={expirationDate}
              onChange={(e) => setExpirationDate(e.target.value)}
              className='option-input'
              required
            />
          </div>

          

          <div className='option-group'>
            <label htmlFor="length">URL Length:</label>
            <input
              type="number"
              id="length"
              min="4"
              max="10"
              value={urlLength}
              onChange={(e) => setUrlLength(Number(e.target.value))}
              className='option-input'
              required
            />
          </div>
          <div className='option-group'>
            <label htmlFor="oneTime">
              <input
                type="checkbox"
                id="oneTime"
                checked={oneTimeClick}
                onChange={(e) => setOneTimeClick(e.target.checked)}
                className='checkbox-input'
              />
              One-time click only
            </label>
          </div>
        </div>
        {error && <p className="error-message">{error}</p>}
        <div className='shortenURL_button'>
          <Button text='shorten' onClick={handleShorten}/>
        </div>
      </div>
      
      {shortenedUrl && <DisplayURL shortenedURL={shortenedUrl} />}
    </div>
  )
}

export default ShortenURL