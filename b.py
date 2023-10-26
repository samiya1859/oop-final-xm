class Bank:
    def __init__(self) -> None:
        self.users=[]
        self.total_balance=0
        self.total_loan_amount=0
        self.loan_featured_enabled=True
        self.bankrrupt=False
    
    def create_account(self,name,email,address,type):
        account_number=len(self.users)+1
        if type=='S':
            user = savingAc(account_number,name,email,address,interest_rate=2)
        elif type=='C':
            user = currentAc(account_number,name,email,address,limit=2000)
        elif type=='A':
            user= adminAc(name,email,address)
        else:
            print('Invalid account type!')
            return
        self.users.append(user)  


    def delete_account(self,em):
        flag=0
        for user in self.users:
            if  user.email==em:
                self.users.remove(user)
                flag=1
                break
            
        if flag==0:
            print('Account not found!')

    def account_list(self):
        for user in self.users:
            print(f'Account email : {user.email}  Name : {user.name}\n')
    
    def get_total_balance(self):
        for user in self.users:
            self.total_balance+=user.balance
        print(f'total balance of bank - {self.total_balance}')
    
    
    def get_total_loan_amount(self):
        print(f'Total loan amount - {self.total_loan_amount}') 
    
    def loan_feature(self,status):
        
        self.loan_featured_enabled=status

    def transfer(self,from_ac,to_ac,amount):
        if from_ac in self.users and to_ac in self.users:
            from_user=self.users[from_ac]
            to_user=self.users[to_ac]

            if from_user.balance>=amount:
                from_user.transfer_balance(to_user,amount)
            else:
                print('Insufficient balance!')   
        else:
            print('account doesnot exist!')
    
    def is_bankrrupt(self,status):
        self.bankrrupt=status
        



    


class User:
    users=[]
    def __init__(self,acnumber,name,email,address,type) -> None:
        self.acnumber=acnumber
        self.name=name
        self.email=email
        self.address=address
        self.type=type
        self.balance=0
        self.loan_count=0
        self.transaction_history=[]
        self.loan_featured_enabled=True
        self.bankrrupt=False
        User.users.append(self)

    def deposit(self,amount):
        if amount>0:
            self.balance+=amount
            self.transaction_history.append(f'Diposited ${amount}')
        else:
            print('Not enough money to deposit!')
        
    
    def withdraw(self,amount):
        if self.bankrrupt==False:
            if amount>0 and amount<=self.balance  :
                self.balance-=amount
                self.transaction_history.append(f'Withdrew ${amount}')
                print(f'Successfully withdrew ${amount}')
            else:
                print('Withdrawal amount exceeded!')
        else:
            print('Bank got bankrrupt! you cannot withdraw.')
    
    def check_balance(self):
        print(f'Your current balance is - {self.balance}') 
        return self.balance
    
    

    def take_loan(self,amount):
        if self.loan_count<2 and self.loan_featured_enabled==True:
            self.balance+=amount
            bank.total_loan_amount +=amount
            self.loan_count+=1
            self.transaction_history.append(f'Loan taken : ${amount}')

        else:
            print('Can not take loan anymore!')

    def transfer_balance(self,to_user,amount):
        flag=0
        for user in self.users:
            if user.email==to_user:
                user.balance+=amount
                self.balance-=amount
                flag=1
                print(f'transferred ${amount} to {to_user}')
                self.transaction_history.append(f'Transferred : ${amount}')
                break
        if flag==0:
            print(f'{to_user} is not a registered user.')
        
      
    
    def check_transaction_history(self):
        for transaction in self.transaction_history:
            print(transaction)
            
             
class savingAc(User):
    def __init__(self, acnumber, name, email, address,interest_rate) -> None:
        super().__init__(acnumber, name, email, address,'Savings')
        self.interest_rate=interest_rate

    def add_interest(self,interest_rate):
        interest= self.balance * (interest_rate/100)
        self.deposit(interest)

class currentAc(User):
    def __init__(self, acnumber, name, email, address, limit) -> None:
        super().__init__(acnumber, name, email, address, 'Current')
        self.limit=limit
    
    def withdraw(self, amount):
        if self.bankrrupt==False:
            if amount>=0 and amount<=(self.balance+self.limit) :
                self.balance-=amount
                print(f'Successfully withdrew ${amount}')
                self.transaction_history.append(f'Withdrew ${amount}')
            else:
                print('\n Invalid amount')
        else:
            print('Bank got bankrrupt! You can not withdraw.')

class adminAc(User):
    def __init__(self,  name, email, address) -> None:
        super().__init__(1, name, email, address, 'admin')
        

        
bank = Bank()
currentuser=None

while(True):
    if(currentuser==None):
        print('-----WELCOME------')
        print('You have to login/register first.')
        ch= input('Enter Login(L) or Register(R)? -')
        if ch=='R':
            name=input('Enter your name - ')
            email=input('Enter your email address - ')
            address=input('Enter your address - ')
            pas=input('Enter your password - ')
            account_type=input('Enter your account type Savings(S) or Current(C) or Admin(A)? ')
            if account_type=='S':
                bank.create_account(name,email,address,account_type)
            elif account_type=='C':
                bank.create_account(name,email,address,account_type)
            elif account_type=='A':
                bank.create_account(name,email,address,account_type)
            else:
                print('Invalid account type')
        elif ch=='L':
            em=input('Enter Your email : ')
            for user in bank.users:
                if em==user.email:
                    currentuser=user
                    break
        else:
            print('You have entered an invalid input!')
    else:
        print(f'----Welcome {currentuser.name} --------')
        if currentuser.type=='Savings':
            print('1. Deposit ')
            print('2. Withdraw ')
            print('3. Apply Interest ')
            print('4. check balance')
            print('5.Take Loan')
            print('6.transfer balance')
            print('7.Check transaction history')
            print('8. Log out')
            
            op=int(input('Enter option no - '))
            if op==1:
                amount = int(input('Enter an amount you want to deposit - '))
                currentuser.deposit(amount)
                print(f'Successfully deposited ${amount}')
            elif op==2:
                if bank.bankrrupt==False:
                    amount=int(input('Enter an amount to withdraw - '))
                    currentuser.withdraw(amount)
                else:
                    print('You can not withdraw any money for bankrrupt!')
                
            elif op==3:
                irate=int(input('Enter interest rate : '))
                currentuser.add_interest(irate)
                print('added interest on your balance.')
            elif op==4:
                currentuser.check_balance()
            elif op==5:
                if bank.loan_featured_enabled==True:
                    ln = int(input('Enter the amount you want to take loan - '))
                    currentuser.take_loan(ln)
                    print(f'Successfully taken loan of  ${ln}')
                else:
                    print('You Can not take any loan')
            elif op==6:
                em=input('Enter the email you want to transfer balance - ')
                am=int(input('Enter the amount - '))
                currentuser.transfer_balance(em,am)
                print(f'Successfully transferred balance to {em} - ${am}')
            elif op==7:
                print('Here is your transaction history - ')
                currentuser.check_transaction_history()
            elif op==8:
                currentuser=None
                print('You have logged out.')
            else:
                print('Please enter a valid option!')
        
        elif currentuser.type=='Current':
            print('1.deposit')
            print('2. withdraw')
            print('3. Check balance')
            print('4.Take loan')
            print('5.Check transaction history')
            print('6. log out' )   
            op = int(input('Enter your option - '))    
            if op==1:
                amount=int(input('Enter amount to deposit - '))
                currentuser.deposit(amount)
                print(f'Successfully deposited ${amount}')
            elif op==2:
                if bank.bankrrupt==False:
                    amount=int(input('Enter an amount to withdraw - '))
                    currentuser.withdraw(amount)
                else:
                    print('You can not withdraw any money for bankrrupt!')
                    
            elif op==3:
                currentuser.check_balance()
            elif op==4:
                if bank.loan_featured_enabled==True:
                    ln = int(input('Enter the amount you want to take loan - '))
                    currentuser.take_loan(ln)
                    print(f'Successfully taken loan of  ${ln}')
                else:
                    print('You Can not take any loan')
            elif op==5:
                print('Here is your transaction history - ')
                currentuser.check_transaction_history()
            elif op==6:
                currentuser=None
                print('You have logged out.')
            else:
                print('Please enter a valid option')
        
        elif currentuser.name=='admin':
            print('1.create account')
            print('2.delete any account')
            print('3.see all account list')
            print('4.check total balance of bank')
            print('5.check total loan amount')
            print('6.loan feature')
            print('7.Bankrrupt')
            print('8.log out' )   
            op=int(input('Enter an option - '))    
            if op==1:
                name=input('Enter the name : ')
                email=input('enter email : ')
                address=input('Enter address : ')
                account_type= input('Enter account type : Savings(S) or Current(C) ?')
                if account_type=='S':
                    bank.create_account(name,email,address,'S')
                    print('Successfully created one Savings account.')
                elif account_type=='C':
                    bank.create_account(name,email,address,'C')
                    print('Successfully created one current account.')
                else:
                    print('Invalid account type')
            
            elif op==2:
                account_mail= input('Enter the account email : ')
                bank.delete_account(account_mail)
                print(f'Suuccesfully deleted the account .')
            
            elif op==3:
                bank.account_list()
            elif op==4:
                total_balance = bank.get_total_balance()
                
            
            elif op==5:
                total_loan_amount= bank.get_total_loan_amount()
                

            elif op==6:
                feature_enabled = input('Enable (E) or Disable(D) loan feature ? ')
                if feature_enabled=='E':
                    bank.loan_feature(True)
                    print('Loan feature is enabled!')
                elif feature_enabled=='D':
                    bank.loan_feature(False)
                    print('loan feature is disabled!')
                else:
                    print('Invalid option')

            elif op==7:
                bnk=input('Type Y if bank is bankrrupt otherwise N : ')
                if(bnk=='Y'):
                    bank.is_bankrrupt(True)
                    print('Bank got bankrrupt!')
                elif(bnk=='N'):
                    bank.is_bankrrupt(False)
                    print('Bank is not bankrrupted.Making transaction is available!')
                else:
                    print('You entered invalid option!')
                    
            elif op==8:
                currentuser=None
                print('You have logged out.')
            else:
                print('Please enter a valid option!')
        else:
            print('Not a valid current user')
    










