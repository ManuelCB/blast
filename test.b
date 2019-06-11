VAR n;0;
LOOP ;

	OP EQUAL;#n;0;
	
	PRINT #n;
	
	LOOP ;
		OP ADD;#n;1;
		PRINT #n;
		IF EQUAL;#n;10;
			PRINT broke;
			BREAK ;
		ENDIF ;
	ENDLOOP ;
	
	PRINT write "end" to end this;
	VAR read;#READ;;
	
	IF EQUAL;#read;end;
		BREAK ;	
	ELSE ;
		PRINT I didn't mean ;#read; !;
		DELVAR read;
	ENDIF ;

ENDLOOP ;

PRINT Success!!;