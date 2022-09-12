import react, {useEffect, useState} from "react"
import {useParams} from "react-router-dom"
import axios from "axios"

import "./chat.css"

const Chat = () => {

	const initial_chat = [
		{text: "Please input words.", user: 0}
	]
	const initial_user = [
		{ id: 0, name: "system" },
		{ id: 1, name: "bot" },
		{ id: 2, name: "user" }
	]

	const { id } = useParams<{id: string}>()
	const [chats, setChats] = useState(initial_chat)
	const [text, setText] = useState<string>("")
	const [loading, setLoading] = useState(false)

	const onChangeTextForm = (e: any) => {
		setText(e.target.value)
	}

	const onClickSendButton = () => {
		setLoading(true)
		appendChat(2, text)
		setText("")
		const splitted_new_text = text.split(" ")
		const new_text = splitted_new_text.join("_")
		axios(`http://localhost:5000/send/${id}/${new_text}`)
		.then((result) => {
			setLoading(false)
			appendChat(1, result.data.text)
		})
	}

	const appendChat = (user_type: number, text: string) => {
		setChats((chats) => {
			const copied_chat = JSON.parse(JSON.stringify(chats))
			console.log(copied_chat)
			copied_chat.push({user: user_type, text: text})
			return copied_chat
		})
	}

	if (!id) {
		return (
			<div>
				<p>ユーザーを指定してください</p>
			</div>
		)
	}

	return (
		<div>
			<p>ユーザーID : {id} 様</p>
			<div className="chat-result-area">
				{ chats.map((chat) => {
					return (
						<>
							<div className={ chat.user === 0
								? "system-user chat-content"
								: chat.user === 1 
								? "bot-user chat-content"
								: "user-user chat-content"								
							}>
									{chat.text}
							</div>
						</>
					)
				})}
			</div>
			<div className="chat-input-area">
				<input
					type="text"
					value={text}
					className="input-form"
					onChange={(e) => onChangeTextForm(e)}
				/>
				<button
					className="input-button"
					onClick={() => onClickSendButton()}
				>
					{ loading
						? "送信中"
						: "送信する"
					}
				</button>
			</div>
		</div>
	)
}

export default Chat;