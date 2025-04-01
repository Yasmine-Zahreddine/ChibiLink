import { useState } from 'react';
import Button from '../button/Button';
import './displayURL.css';

interface DisplayURLProps {
  shortenedURL: string;
}

const DisplayURL = ({ shortenedURL }: DisplayURLProps) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(shortenedURL);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  return (
    <div className="display-url">
      <div className="url-container">
        <p className="url-label">Here's your Chibi Link</p>
        <p className="shortened-url">{shortenedURL}</p>
      </div>
      <div className='url-button'>
        <Button
            text={copied ? "Copied!" : "Copy"} 
            onClick={handleCopy}
        />
      </div>
    </div>
  );
};

export default DisplayURL;