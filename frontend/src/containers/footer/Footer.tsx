import './footer.css'
import logo from '../../assets/logo_dark.png'

const Footer = () => {
  return (
    <div className='footer section_padding'>
      <div className='footer-links'>
        <div className='footer-links_logo'>
          <img src={logo} alt="ChibiLink Logo"/>
          <p>Where long URLs become pocket-sized links</p>
        </div>
        <div className='footer-links_div'>
          <h4>About ChibiLink</h4>
          <p>A simple and fast URL shortener</p>
          <p>No registration required</p>
          <p>Free to use</p>
          <p>Currently in development - more features coming soon!</p>
        </div>
        <div className='footer-links_div'>
          <h4>Usage Guidelines</h4>
          <p>No illegal content</p>
          <p>Maximum 5 requests per minute</p>
          <p>Only HTTPS/HTTP URLs supported</p>
        </div>
        <div className='footer-links_div'>
          <h4>Contact</h4>
          <p>Developer: Yasmine Zahreddine</p>
          <p><a href="mailto:zahreddineyasmine@gmail.com">zahreddineyasmine@gmail.com</a></p>
          <p><a href="https://github.com/Yasmine-Zahreddine" target="_blank" rel="noopener noreferrer">Github</a></p>
        </div>
      </div>
      <div className='footer-copyright'>
        <p>© {new Date().getFullYear()} ChibiLink. All rights reserved.</p>
      </div>
    </div>
  )
}

export default Footer