// // import { checkToken } from "@/api/authAPI";
// import { reset } from "@/hooks/redux/slice";
// import { useMutation } from "@tanstack/react-query";
// // import type { T } from "node_modules/react-router/dist/development/context-DSyS5mLj.d.mts";
// import { useEffect } from "react";
// import { useCookies } from "react-cookie";
// import { useDispatch } from "react-redux";
// import { useNavigate } from "react-router";


// export default function WithoutAuth(WrappedComponent: React.ComponentType<T>) {
//     return () => {
//         const nav = useNavigate()
//         const dispatch = useDispatch()
//         const [cookies, _, removeCookie] = useCookies() 

//         const tokenMutate = useMutation({
//             mutationFn: ({ token }: { token: string }) => checkToken(token),
//             onSuccess: () => {
//                 nav("/main")
//             },
//             onError: () => {
//                 dispatch(reset())
//                 removeCookie("token")
//             }
//         })

//         useEffect(() => {
//             cookies?.token ?
//                 tokenMutate.mutate({ token: cookies?.token })
//             : null
//         }, [])

//         return <WrappedComponent/>
//     }
// }