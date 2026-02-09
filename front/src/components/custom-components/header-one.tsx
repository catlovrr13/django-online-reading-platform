import '@/App.css'

export function HeaderOne({cl, text}:{cl?:string|null, text: string|null}){
    return <h1 className={`text-4xl font-test ${cl}`}>{text}</h1>
}