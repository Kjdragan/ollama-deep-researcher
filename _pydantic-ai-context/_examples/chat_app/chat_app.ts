// BIG FAT WARNING: to avoid the complexity of npm, this typescript is compiled in the browser
// there's currently no static type checking

// @ts-ignore: External module without types
import { marked } from 'https://cdnjs.cloudflare.com/ajax/libs/marked/15.0.0/lib/marked.esm.js'

// Get DOM elements with null checks
const convElement = document.getElementById('conversation')
if (!convElement) throw new Error('Conversation element not found')

const promptInput = document.getElementById('prompt-input') as HTMLInputElement
if (!promptInput) throw new Error('Prompt input not found')

const spinner = document.getElementById('spinner')
if (!spinner) throw new Error('Spinner element not found')

const errorElement = document.getElementById('error')
if (!errorElement) throw new Error('Error element not found')

// After null checks, we can safely use these elements with non-null assertion
const elements = {
    conversation: convElement!,
    prompt: promptInput!,
    spinner: spinner!,
    error: errorElement!
}

// stream the response and render messages as each chunk is received
// data is sent as newline-delimited JSON
async function onFetchResponse(response: Response): Promise<void> {
  let text = ''
  let decoder = new TextDecoder()
  if (response.ok && response.body) {
    const reader = response.body.getReader()
    while (true) {
      const {done, value} = await reader.read()
      if (done) {
        break
      }
      text += decoder.decode(value)
      addMessages(text)
      elements.spinner.classList.remove('active')
    }
    addMessages(text)
    elements.prompt.disabled = false
    elements.prompt.focus()
  } else {
    const text = await response.text()
    console.error(`Unexpected response: ${response.status}`, {response, text})
    throw new Error(`Unexpected response: ${response.status}`)
  }
}

// The format of messages, this matches pydantic-ai both for brevity and understanding
// in production, you might not want to keep this format all the way to the frontend
interface Message {
  role: string
  content: string
  timestamp: string
}

// take raw response text and render messages into the `#conversation` element
// Message timestamp is assumed to be a unique identifier of a message, and is used to deduplicate
// hence you can send data about the same message multiple times, and it will be updated
// instead of creating new message elements
function addMessages(responseText: string) {
  const lines = responseText.split('\n')
  const messages: Message[] = lines.filter(line => line.length > 1).map(j => JSON.parse(j))
  for (const message of messages) {
    // we use the timestamp as a crude element id
    const {timestamp, role, content} = message
    const id = `msg-${timestamp}`
    let msgDiv = document.getElementById(id)
    if (!msgDiv) {
      msgDiv = document.createElement('div')
      msgDiv.id = id
      msgDiv.title = `${role} at ${timestamp}`
      msgDiv.classList.add('border-top', 'pt-2', role)
      elements.conversation.appendChild(msgDiv)
    }
    // @ts-ignore: marked.parse exists but TS doesn't know about it
    msgDiv.innerHTML = marked.parse(content)
  }
  window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
}

function onError(error: unknown) {
  console.error(error)
  elements.error.classList.remove('d-none')
  elements.spinner.classList.remove('active')
}

async function onSubmit(e: SubmitEvent): Promise<void> {
  e.preventDefault()
  elements.spinner.classList.add('active')
  const form = e.target as HTMLFormElement
  const body = new FormData(form)

  elements.prompt.value = ''
  elements.prompt.disabled = true

  const response = await fetch('/chat/', {method: 'POST', body})
  await onFetchResponse(response)
}

// call onSubmit when the form is submitted (e.g. user clicks the send button or hits Enter)
const form = document.querySelector('form')
if (!form) throw new Error('Form element not found')
form.addEventListener('submit', (e) => onSubmit(e).catch(onError))

// load messages on page load
fetch('/chat/').then(onFetchResponse).catch(onError)