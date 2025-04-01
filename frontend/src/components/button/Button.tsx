import './button.css'
interface ButtonProps {
  text: string;
  onClick?: () => void;
}

function Button({ text, onClick }: ButtonProps) {
  return (
    <button  
      onClick={onClick}
    >
      {text}
    </button>
  )
}

export default Button