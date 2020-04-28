export type Meme = {
  img: HTMLImageElement
  id: number
  imageDescription: string
  textDescription: string
}

export type UnloadedMeme =
| { type: 'native', id: number, url: string }
| { type: 'external', url: string }

// TODO: make this global / union this with `Meme` ???
export type FeedMeme = {
  id: number,
  url: string, 
  likes: number,
  dislikes: number
}

export type User = {
  id: number
  username: string
}

export type AuthState =
| { readonly status: 'unknown' | 'no' }
| { status: 'yes', user: User, token: string }

export enum Repo {
  Own, Public
}

export type Tag = {
  id: number
  tag: string
}

export type SearchRequest = {
  own: boolean
} & (
  | { extended: false, q: string }
  | { extended: true, tags: Tag[], qText: string, qImage: string }
)