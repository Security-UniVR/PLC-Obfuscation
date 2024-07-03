FUNCTION_BLOCK rand_generator
  VAR_INPUT
    IN : BOOL;
  END_VAR
  VAR
    M : BOOL := 0;
    INIT : BOOL := 0;
  END_VAR
  VAR_OUTPUT
    OUT : INT := 0;
  END_VAR

  (* Initialize our random generator *)
  (* This IF is called only the first time this *)
  (* block executes *)
  IF INIT = 0 THEN
    {
    srand(17);}
    INIT := 1;
  END_IF;

  IF M = 0 and IN = 1 THEN
    (* Using pragma to write code directly in C. *)
    (* You can access your PLC program variables using *)
    (* GetFbVar(var,...) and SetFbVar(var,val,...) calls *)
    {SetFbVar(OUT,  rand() % 1000 )}

    
  END_IF;
  M := IN;
END_FUNCTION_BLOCK
