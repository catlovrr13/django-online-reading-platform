export function Header1({cl, text}:{cl?:string|null, text: string|null}){
    return <h1 className={`text-3xl font-bold ${cl}`}>{text}</h1>
}

export function Header2({cl, text}:{cl?:string|null, text: string|null}){
    return <h1 className={`text-2xl font-bold ${cl}`}>{text}</h1>
}

export function Header3({cl, text}:{cl?:string|null, text: string|null}){
    return <h1 className={`text-xl font-semibold ${cl}`}>{text}</h1>
}