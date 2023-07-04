  /bids/{bid_id}:
# --------------------------------------------
    get:
      tags:
        - bids
      summary: Returns a single bid
      description: Returns a single bid
      operationId: get_bid
      parameters:
        - name: bid_id
          in: path
          description: ID of bid to return
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: A single bid
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Bid'
        '404':
          description: Bid not found
          content:
            application/json:
              schema:
                type: object
                example: {
                  "Error": "Bid not found"
                }
        '500':
          $ref: '#/components/responses/InternalServerError'
# --------------------------------------------




# --------------------------------------------
# Schemas
     _id:
          type: string
          format: uuid
          example: "9af94206-adff-476c-b2f9-ed7be3468944"