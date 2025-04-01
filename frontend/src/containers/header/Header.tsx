import "./header.css"
import logo from "../../assets/logo.png"
import ShortenURL from "../../components/shortenURL/ShortenURL"
function Header() {
  return (
    <div className="header">
        <div className="header_img">
            <img src={logo}/>
            <p>Big links? We make them chibi!</p>
        </div>
        <div className="header_shortener">
          <ShortenURL/> 
        </div>
    </div>
  )
}

export default Header