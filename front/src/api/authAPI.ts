const URL = "http://127.0.0.1:8000/api"

export const loginUser = async (data: {username: string, password: string}) => {
    let result
    try {
        const response = await fetch(`${URL}/token/`, {
            method: "POST",
            headers: {
                Accept: 'application/json',
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })

        const text = await response.text()

        try {
            result = JSON.parse(text)
        } catch (e) {
            console.error('Failed to parse response:', text)
            throw new Error('Server returned invalid JSON: ' + text.substring(0, 50))
        }

        if (!response.ok) {
            throw new Error(result.detail || 'Login failed')
        }

        return {
            token: result.access,
            refresh: result.refresh,
            username: data.username
        }
    } catch (error: any) {
        console.error('Login error:', error)
        throw error
    }
}

export const getUserProfile = async (token: string) => {
    const response = await fetch(`${URL}/profile/`, {
        method: "GET",
        headers: {
            Accept: 'application/json',
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    })

    if (!response.ok) {
        throw new Error('Failed to fetch user profile')
    }

    return await response.json()
}

// export const registerUser = async 