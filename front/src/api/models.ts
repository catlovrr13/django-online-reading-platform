export type Res = {
    ok: boolean;
    errors?: [] | null;
    data?: any;
    message?: string;
    others?: [];
    token?: string;
}

export type User = {
    id: number;
    username:string;
    email: string;
    email_verified_at: Date;
    created_at:Date;
    updated_at: Date;
    role_names: Array<string>,
    token: string; 
}

