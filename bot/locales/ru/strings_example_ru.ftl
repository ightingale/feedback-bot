start-text =
    Здравствуйте!
    На связи техподдержка бота { $bot_info }.

    Напишите свой вопрос

no =
    { $capitalization ->
       *[lowercase] нет
        [capitalized] Нет
    }

yes =
    { $capitalization ->
       *[lowercase] да
        [capitalized] Да
    }

new-topic-intro =
    { $name }
    ├── Наличие бана: { $ban_status }
    ├── Telegram ID: <code>{ NUMBER($id, useGrouping: 0) }</code>
    ├── Юзернейм: { $username }
    └── Язык: { $language_code }

error-cannot-find-user =
    Ошибка: не удалось найти пользователя для этого топика. Сообщение не доставлено.

error-cannot-deliver-to-forum =
    Ошибка: не удалось доставить ваше сообщение до получателя. Попробуйте снова через несколько минут.


banned-successfully = Пользователь забанен. Отныне на все входящие сообщения бот будет автоматически отвечать уведомлением о блокировке.
shadowbanned-successfully = Пользователь добавлен в список тихой блокировки. Отныне все входящие сообщения будут игнорироваться ботом.

ban-status-ban = блокировка
ban-status-shadowban = тихая блокировка
ban-status-unknown = неизвестный тип

you-are-banned = Вы были заблокированы владельцем бота. Ваши сообщения не будут доставлены.


already-banned = Пользователь уже был забанен ранее.
already-shadowbanned = Пользователь уже был добавлен в список тихой блокировки ранее.
already-shadowbanned-before = Пользователь уже находится в списке тихой блокировки. Автоматические ошибки отправляться не будут.

any-ban-error = Ошибка при блокировке пользователя. Попробуйте повторить позднее.

unban-not-needed = Пользователь не заблокирован.
unbanned-successfully = Пользователь разбанен.
any-unban-error = Ошибка при разблокировке пользователя. Попробуйте повторить позднее.

user-info-update-success = Информация о пользователе успешно обновлена: проверьте первое сообщение топика.
user-info-update-error = Ошибка при обновлении информации о пользователе. Попробуйте повторить позднее.

topic-ignored = Этот топик помечен как игнорируемый; он не связан ни с одним пользователем.
