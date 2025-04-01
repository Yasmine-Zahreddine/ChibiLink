import './button.css'
interface ButtonProps {
  text: string;
  onClick?: () => void;
}

function Button({ text, onClick }: ButtonProps) {
  return (
    <button  
      className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
      onClick={onClick}
    >
      {text}
    </button>
  )
}

export default Button