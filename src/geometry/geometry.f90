module geometry
    use precision, only: wp
    use maths_utils, only: norm
    private


    !> Type Atom
    type atom_type
        !TODO(Alex) Check out how private affects type access
        ! private
        !> Position in angstrom
        real(wp), dimension(3) :: position
        !> Species label
        character(len=3) :: symbol
        !> Atomic number
        integer :: an
    end type atom_type


    interface distance_matrix
        module procedure distance_matrix_from_positions, distance_matrix_from_molecule
    end interface distance_matrix


    public :: distance_matrix


contains

    !TODO(Alex) Code up some test systems (crystals)
    !type(atom_type) function

    !> @brief
    !> For an array of atoms, construct a distance matrix
    !> @param[in] molecule
    function distance_matrix_from_positions(positions) result(d)
        real(wp), intent(in) :: positions(:,:)
        real(wp), allocatable :: d(:,:)
        integer :: ia, ja, n_atoms

        n_atoms = size(positions)
        allocate(d(n_atoms, n_atoms))

        do ia = 1, n_atoms
            do ja = ia, n_atoms
                d(ia, ja) = norm(positions(ja, :) - positions(ia, :))
                d(ja, ia) = d(ia, ja)
            enddo
        enddo

    end function distance_matrix_from_positions

    !> @brief
    !> For an array of atoms, construct a distance matrix
    !
    !> Would ideally wrap distance_matrix_from_positions but
    !> then I need to write another routine to create an array of positions
    !> from molecule
    !
    !> @param[in] molecule
    function distance_matrix_from_molecule(molecule) result(d)
        type(atom_type), intent(in) :: molecule(:)
        real(wp), allocatable :: d(:,:)
        integer :: ia, ja, n_atoms
        real(wp) :: r_a(3)

        n_atoms = size(molecule)
        allocate(d(n_atoms, n_atoms))

        do ia = 1, n_atoms
            r_a = molecule(ia)%position
            do ja = ia, n_atoms
                d(ia, ja) = norm(molecule(ib)%position - r_a)
                d(ja, ia) = d(ia, ja)
            enddo
        enddo

    end function distance_matrix_from_molecule

end module geometry