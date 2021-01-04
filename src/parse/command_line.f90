module command_line
    use precision, only: dp
    implicit none
    private

    !> All arguments that can be passed via the command line to the main code
    type cmd_line_args_type
        !> Input file
        character(len=50) :: input_file
        ! Could add additional arguments
        contains
            !> Parse arguments from the command line. i.e. initialise
            procedure :: parse => parse_command_line_args
    end type cmd_line_args_type


    public :: cmd_line_args_type

contains

    !> Parse arguments from the command line
    subroutine parse_command_line_args(this)
        class(cmd_line_args_type), intent(inout) :: this

        if (command_argument_count() < 1) then
            write(*, *) 'error. Expecting a command line argument file input'
            stop
        else if (command_argument_count() > 1) then
            write(*, *) 'error. Code only accepts a single command line argument, for input'
            stop
        end if

        call get_command_argument(1, this%input_file)

        ! If one needs to convert string to real:
        ! READ(arg1, *) num1 !where num1 is the real

    end subroutine


end module command_line