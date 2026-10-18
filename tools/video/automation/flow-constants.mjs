// Constants both the worker's flow and the brand story's steps read, kept apart from flow.mjs so
// story.mjs does not import the module that imports it.

// The storytelling panel rides on the verifier stage under its own variant: the server keeps a
// model call as "<stage>/<variant>" in 32 characters, and the API's stage names are a closed list.
export const NARRATIVE_VARIANT = "narrative";
