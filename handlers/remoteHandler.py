## built-in modules

## custom modules
from modules.toolkit import toolkit
from modules.fileEnsurer import fileEnsurer
from handlers.connectionHandler import connectionHandler
from handlers.memberHandler import memberHandler

class remoteHandler():

    """
    
    The handler that handles all interactions with the remote storage.\n

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, file_ensurer:fileEnsurer, toolkit:toolkit) -> None:

        """
        
        Initializes the remoteHandler class.\n

        Parameters:\n
        file_ensurer (object - fileEnsurer) : The fileEnsurer object.\n
        toolkit (object - toolkit) : The toolkit object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        self.file_ensurer = file_ensurer

        self.toolkit = toolkit

        self.connection_handler = connectionHandler(self.file_ensurer, self.toolkit)

        self.member_handler = memberHandler(self.file_ensurer, self.toolkit, self.connection_handler)

        ##----------------------------------------------------------------dir----------------------------------------------------------------


        ##----------------------------------------------------------------paths----------------------------------------------------------------


        ##----------------------------------------------------------------variables----------------------------------------------------------------
        

        ##----------------------------------------------------------------functions---------------------------------------------------------------- 

##--------------------start-of-reset_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def reset_remote_storage(self, is_forced:bool, forced_by:str | None = None) -> None:

        """
        
        Resets the remote storage with the local storage.\n
        Note that this will reset all the words remotely stored on the connected database.\n
        Use Carefully!\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        await self.delete_remote_storage()
        await self.create_remote_storage()
        await self.fill_remote_storage()

        if(is_forced):
            await self.file_ensurer.logger.log_action("INFO", "remoteHandler", f"Remote storage has been forcibly reset by {forced_by}.")

        else:
            await self.file_ensurer.logger.log_action("INFO", "remoteHandler", "Remote storage has been reset.")

##--------------------start-of-delete_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def delete_remote_storage(self) -> None:

        """
        
        Deletes the remote storage.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------members----------------------------------------------------------------

        delete_members_query = """
        drop table if exists members
        """

        ##----------------------------------------------------------------calls----------------------------------------------------------------

        await self.connection_handler.execute_query(delete_members_query)

##--------------------start-of-create_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def create_remote_storage(self) -> None:

        """
        
        Creates the tables for the remote storage.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------members----------------------------------------------------------------

        create_members_query = """
        create table if not exists members (
            member_id bigint primary key,
            member_name varchar(32) not null,
            spin_scores varchar(32) not null,
            credits int not null
        )
        """

        ##----------------------------------------------------------------calls----------------------------------------------------------------

        await self.connection_handler.execute_query(create_members_query)


##--------------------start-of-fill_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def fill_remote_storage(self) -> None:

        """
        
        Fills the remote storage with the local storage.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------members----------------------------------------------------------------

        async def fill_members():

            table_name = "members"

            for member in self.member_handler.members:

                new_id = member.member_id
                new_name = member.member_name
                new_spin_scores = str(member.spin_scores)
                new_credits = member.credits

                table_name = "members"
                insert_dict = {
                    "member_id" : new_id,
                    "member_name" : new_name,
                    "spin_scores" : new_spin_scores,
                    "credits" : new_credits
                }

                await self.connection_handler.insert_into_table(table_name, insert_dict)

        ##----------------------------------------------------------------calls----------------------------------------------------------------

        await fill_members()