export type Meme = {
  img: HTMLImageElement
  id: number
  imageDescription: string
  textDescription: string
}

export type UnloadedMeme = {
  id: number
}

export type UnloadedForeignMeme = {
  url: string
}

export type SnackbarError = {
  msg: string
  short: boolean
}

export type User = {
  id: number
  username: string
}

export type AuthState =
| { readonly status: 'unknown' | 'no' }
| { status: 'yes', user: User }

export enum Repo {
  Own, Public
}