import Button from '../button/Button'
import './shortenURL.css'
function ShortenURL() {
  return (
    <div className='shortenURL'>
        <input type="text" placeholder="Enter your URL here" className='shortenURL_input' />
        <div className='shortenURL_button'>
            <Button text='shorten' onClick={() => {}}/>
        </div>
    </div>
  )
}

export default ShortenURL